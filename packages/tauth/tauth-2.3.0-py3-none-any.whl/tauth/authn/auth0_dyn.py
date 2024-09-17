from typing import Any, Optional, Self

import jwt as pyjwt
from cachetools.func import ttl_cache
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from fastapi import BackgroundTasks, HTTPException, Request
from httpx import Client, HTTPError
from jwt import (
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
    PyJWKClient,
    PyJWKSet,
)
from loguru import logger
from pydantic import BaseModel
from redbaby.pyobjectid import PyObjectId

from ..authproviders.models import AuthProviderDAO
from ..entities.models import EntityDAO
from ..entities.schemas import EntityIntermediate
from ..schemas import Creator, Infostar
from ..utils import creation, reading
from .utils import TimedCache


def get_token_headers(token: str) -> dict[str, Any]:
    header = pyjwt.get_unverified_header(token)
    return header


def get_token_unverified_claims(token: str) -> dict[str, Any]:
    claims = pyjwt.decode(token, options={"verify_signature": False})
    return claims


def get_signing_key(kid: str, domain: str) -> Optional[str]:
    jwk_set = ManyJSONKeySetStore.get_jwks(domain)
    signing_key = PyJWKClient.match_kid(jwk_set.keys, kid)
    if isinstance(signing_key, RSAPrivateKey):
        return signing_key.key.public_key()
    return signing_key.key if signing_key else None


class Auth0Settings(BaseModel):
    domain: str
    audience: str

    @classmethod
    def from_authprovider(cls, authprovider: AuthProviderDAO) -> Self:
        iss = authprovider.get_external_id("issuer")
        if not iss:
            raise MissingRequiredClaimError("iss")
        aud = authprovider.get_external_id("audience")
        if not aud:
            raise MissingRequiredClaimError("aud")
        return cls(domain=iss, audience=aud)


class ManyJSONKeySetStore:
    @classmethod
    @ttl_cache(maxsize=32, ttl=60 * 60 * 6)
    def get_jwks(cls, domain: str) -> PyJWKSet:
        logger.debug(f"Fetching JWKS from {domain}.")
        with Client() as client:
            res = client.get(f"{domain}.well-known/jwks.json")
        try:
            res.raise_for_status()
        except HTTPError as e:
            logger.error(f"Failed to fetch JWKS from {domain}.")
            raise e

        return PyJWKSet.from_dict(res.json())


class RequestAuthenticator:
    CACHE: TimedCache[str, tuple[Infostar, str, dict]] = TimedCache(
        max_size=4096,
        ttl=60 * 60 * 1,  # 1h
    )

    @staticmethod
    def get_authprovider(token_value: str) -> AuthProviderDAO:
        logger.debug("Getting AuthProvider.")
        filters: dict[str, Any] = {"type": "auth0"}

        token_claims = get_token_unverified_claims(token_value)

        matches = []
        if aud := token_claims.get("aud"):
            # We assume that the actual audience is the first element in the list.
            # The second element is the issuer's "userinfo" endpoint.
            matches.append(
                {
                    "$elemMatch": {"name": "audience", "value": aud[0]},
                }
            )

        if org_id := token_claims.get("org_id"):
            matches.append(
                {
                    "$elemMatch": {"name": "org_id", "value": org_id},
                }
            )

        if matches:
            if len(matches) > 1:
                filters["external_ids"] = {"$all": matches}
            else:
                filters["external_ids"] = matches[0]

        provider = reading.read_one_filters(
            infostar={}, model=AuthProviderDAO, **filters
        )  # type: ignore
        return provider

    @staticmethod
    def validate_access_token(
        token_value: str,
        token_headers: dict[str, Any],
        authprovider: AuthProviderDAO,
    ) -> dict:
        logger.debug("Validating access token.")
        sets = Auth0Settings.from_authprovider(authprovider)
        kid = token_headers.get("kid")
        if kid is None:
            raise InvalidTokenError("Missing 'kid' header.")

        signing_key = get_signing_key(kid, sets.domain)
        if signing_key is None:
            raise InvalidSignatureError("No signing key found.")

        access_claims = pyjwt.decode(
            token_value,
            signing_key,
            algorithms=[token_headers.get("alg", "RS256")],
            issuer=sets.domain,
            audience=sets.audience,
            options={"require": ["exp", "iss", "aud"]},
        )
        return access_claims

    @staticmethod
    def validate_id_token(
        token_value: str,
        token_headers: dict[str, Any],
        authprovider: AuthProviderDAO,
    ) -> dict:
        logger.debug("Validating ID token.")
        sets = Auth0Settings.from_authprovider(authprovider)
        kid = token_headers.get("kid")
        if kid is None:
            raise InvalidTokenError("Missing 'kid' header.")

        signing_key = get_signing_key(kid, sets.domain)
        if signing_key is None:
            raise InvalidSignatureError("No signing key found.")

        id_claims = pyjwt.decode(
            token_value,
            signing_key,
            algorithms=[token_headers.get("alg", "RS256")],
            issuer=sets.domain,
            options={"require": ["iss", "exp"], "verify_aud": False},
        )
        return id_claims

    @staticmethod
    def assemble_user_data(access_claims, id_claims) -> dict:
        logger.debug("Assembling user data.")
        required_access = ["org_id"]
        required_id = ["sub", "email"]
        for required_claims, claims in zip(
            [required_access, required_id], (access_claims, id_claims)
        ):
            for c in required_claims:
                if c not in claims:
                    raise MissingRequiredClaimError(c)

        user_data = {
            "user_id": id_claims.get("sub"),
            "user_email": id_claims.get("email"),
        }
        return user_data

    @staticmethod
    def assemble_creator(infostar: Infostar) -> Creator:
        logger.debug("Assembling Creator based on Infostar.")
        c = Creator(
            client_name=f"{infostar.user_owner_handle}/{infostar.service_handle}",
            token_name=infostar.apikey_name,
            user_email=infostar.user_handle,
            user_ip=infostar.client_ip,
        )
        return c

    @staticmethod
    def assemble_infostar(
        request: Request, user_data: dict, authprovider: AuthProviderDAO
    ) -> Infostar:
        logger.debug("Assembling Infostar.")
        if request.client is not None:
            ip = request.client.host
        elif request.headers.get("x-tauth-ip"):
            ip = request.headers["x-tauth-ip"]
        elif request.headers.get("x-forwarded-for"):
            ip = request.headers["x-forwarded-for"]
        else:
            raise HTTPException(
                500,
                detail="Client's IP was not found in: request.client.host, X-Tauth-IP, X-Forwarded-For.",
            )

        infostar = Infostar(
            request_id=PyObjectId(),
            apikey_name="jwt",
            authprovider_type=authprovider.type,
            authprovider_org=authprovider.organization_ref.handle,
            extra={},
            service_handle=authprovider.service_ref.handle,  # TODO: azp
            user_handle=user_data["user_email"],
            user_owner_handle=authprovider.organization_ref.handle,
            client_ip=ip,
            original=None,
        )

        return infostar

    @classmethod
    def validate(
        cls,
        request: Request,
        token_value: str,
        id_token: str,
        background_tasks: BackgroundTasks,
    ):
        key = f"token_value={token_value}&id_token={id_token}"
        cached_value = cls.CACHE.get(key)
        if cached_value:
            infostar, user_email, auth_provider_org_ref = cached_value
        else:
            try:
                header = get_token_headers(token_value)

                authprovider = cls.get_authprovider(token_value)
                access_claims = cls.validate_access_token(
                    token_value, header, authprovider
                )
                id_claims = cls.validate_id_token(id_token, header, authprovider)
            except (
                MissingRequiredClaimError,
                InvalidTokenError,
                InvalidSignatureError,
                HTTPError,
            ) as e:
                raise HTTPException(
                    401,
                    detail={
                        "loc": ["headers", "Authorization"],
                        "msg": f"{e.__class__.__name__}: {e}",
                        "type": e.__class__.__name__,
                    },
                )

            user_data = cls.assemble_user_data(access_claims, id_claims)
            infostar = cls.assemble_infostar(request, user_data, authprovider)
            user_email = user_data["user_email"]
            auth_provider_org_ref = authprovider.organization_ref.model_dump()

            cls.CACHE[key] = (infostar, user_email, auth_provider_org_ref)

        request.state.infostar = infostar
        request.state.creator = cls.assemble_creator(infostar)

        def callback():
            try:
                filters = {
                    "type": "user",
                    "handle": user_email,
                    "owner_ref.handle": auth_provider_org_ref["handle"],
                }
                reading.read_one_filters(infostar=infostar, model=EntityDAO, **filters)
            except HTTPException as e:
                if e.status_code in (404, 409):
                    user_i = EntityIntermediate(
                        handle=user_email,
                        owner_ref=auth_provider_org_ref,  # type: ignore
                        type="user",
                    )
                    creation.create_one(user_i, EntityDAO, infostar=infostar)
                else:
                    logger.error(e)

        background_tasks.add_task(callback)
