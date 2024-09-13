from flask import Response, request, jsonify
from logging import Logger
from pypomes_core import APP_PREFIX, env_get_str, env_get_bytes, env_get_int
from pypomes_crypto import crypto_generate_rsa_keys
from secrets import token_bytes
from typing import Any, Final, Literal

from .jwt_data import JwtData, _get_claims

JWT_ACCESS_MAX_AGE: Final[int] = env_get_int(key=f"{APP_PREFIX}JWT_ACCESS_MAX_AGE",
                                             def_value=3600)
JWT_REFRESH_MAX_AGE: Final[int] = env_get_int(key=f"{APP_PREFIX}_JWT_REFRESH_MAX_AGE",
                                              def_value=43200)
JWT_HS_SECRET_KEY: Final[bytes] = env_get_bytes(key=f"{APP_PREFIX}JWT_HS_SECRET_KEY",
                                                def_value=token_bytes(32))

__priv_key: str = env_get_str(key=f"{APP_PREFIX}JWT_RSA_PRIVATE_KEY")
__pub_key: str = env_get_str(key=f"{APP_PREFIX}JWT_RSA_PUBLIC_KEY")
if not __priv_key or not __pub_key:
    (__priv_key, __pub_key) = crypto_generate_rsa_keys(key_size=2048)
JWT_RSA_PRIVATE_KEY: Final[str] = __priv_key
JWT_RSA_PUBLIC_KEY: Final[str] = __pub_key

# the JWT data object
__jwt_data: JwtData = JwtData()


def jwt_set_service_access(claims: dict[str, Any],
                           service_url: str,
                           auth_type: Literal["HS256", "HS512", "RSA256", "RSA512"] = "HS256",
                           access_max_age: int = JWT_ACCESS_MAX_AGE,
                           refresh_max_age: int = JWT_REFRESH_MAX_AGE,
                           secret_key: bytes = JWT_HS_SECRET_KEY,
                           private_key: str = JWT_RSA_PRIVATE_KEY,
                           public_key: str = JWT_RSA_PUBLIC_KEY,
                           request_timeout: int = None,
                           local_provider: bool = False,
                           logger: Logger = None) -> None:
    """
    Set the data needed to obtain JWT tokens from *service_url*.

    :param claims: the JWT claimset, as key-value pairs
    :param service_url: the reference URL
    :param auth_type: the authentication type
    :param access_max_age: token duration, in seconds
    :param refresh_max_age: duration for the refresh operation, in seconds
    :param secret_key: secret key for HS authentication
    :param private_key: private key for RSA authentication
    :param public_key: public key for RSA authentication
    :param request_timeout: timeout for the requests to the service URL
    :param local_provider: whether 'service_url' is a local endpoint
    :param logger: optional logger
    """
    __jwt_data.add_access_data(claims=claims,
                               service_url=service_url,
                               auth_type=auth_type,
                               access_max_age=access_max_age,
                               refresh_max_age=refresh_max_age,
                               secret_key=secret_key,
                               private_key=private_key,
                               public_key=public_key,
                               request_timeout=request_timeout,
                               local_provider=local_provider,
                               logger=logger)


def jwt_remove_service_access(service_url: str,
                              logger: Logger = None) -> None:
    """
    Remove from storage the access data for *service_url*.

    :param service_url: the reference URL
    :param logger: optional logger
    """
    __jwt_data.remove_access_data(service_url=service_url,
                                  logger=logger)


def jwt_get_token(errors: list[str],
                  service_url: str,
                  logger: Logger = None) -> str:
    """
    Obtain and return a JWT token from *service_url*.

    :param errors: incidental error messages
    :param service_url: the reference URL
    :param logger: optional logger
    :return: the JWT token, or 'None' if an error ocurred
    """
    # inicialize the return variable
    result: str | None = None

    try:
        token_data: dict[str, Any] = __jwt_data.get_token_data(service_url=service_url,
                                                               logger=logger)
        result = token_data.get("access_token")
    except Exception as e:
        if logger:
            logger.error(msg=repr(e))
        errors.append(repr(e))

    return result


def jwt_get_token_data(errors: list[str],
                       service_url: str,
                       logger: Logger = None) -> dict[str, Any]:
    """
    Obtain and return the JWT token associated with *service_url*, along with its expiration timestamp.

    Structure of the return data:
    {
      "access_token": <jwt-token>,
      "expires_in": <seconds-to-expiratio>
    }

    :param errors: incidental error messages
    :param service_url: the reference URL for obtaining JWT tokens
    :param logger: optional logger
    :return: the JWT token data, or 'None' if error
    """
    # inicialize the return variable
    result: dict[str, Any] | None = None

    try:
        result = __jwt_data.get_token_data(service_url=service_url,
                                           logger=logger)
    except Exception as e:
        if logger:
            logger.error(msg=repr(e))
        errors.append(repr(e))

    return result


def jwt_get_claims(errors: list[str],
                   token: str,
                   logger: Logger = None) -> dict[str, Any]:
    """
    Obtain and return the claimset of a JWT *token*.

    :param errors: incidental error messages
    :param token: the token to be inspected for claims
    :param logger: optional logger
    :return: the token's claimset, or 'None' if error
    """
    # initialize the return variable
    result: dict[str, Any] | None = None

    try:
        result = _get_claims(token=token)
    except Exception as e:
        if logger:
            logger.error(msg=repr(e))
        errors.append(repr(e))

    return result


def jwt_verify_request(request: request,
                       logger: Logger = None) -> Response:
    """
    Verify wheher the HTTP *request* has the proper authorization, as per the JWT standard.

    :param request: the request to be verifies
    :param logger: optional logger
    :return: 'None' if the request is valid, otherwise a 'Response' object reporting the error
    """
    # initialize the return variable
    result: Response | None = None

    # retrieve the authorization from the request header
    auth_header: str = request.headers.get("Authorization")

    # was a 'Bearer' authorization obtained ?
    if auth_header and auth_header.startswith("Bearer "):
        # yes, extract and validate the JWT token
        token: str = auth_header.split(" ")[1]
        try:
            _get_claims(token=token)
        except Exception as e:
            # validation failed
            if logger:
                logger.error(msg=repr(e))
            result = Response(response=repr(e),
                              status=401)
    else:
        # no, report the error
        result = Response(response="Authorization failed, as no JWT token was provided",
                          status=401)

    return result


# @flask_app.route(rule="/jwt",
#                  methods=["GET"])
def jwt_service() -> Response:
    """
    Entry point for obtaining JWT tokens.

    Structure of return data:
    {
      "access_token": <jwt-token>,
      "expires_in": <seconds>
    }

    :return: the requested JWT token
    """
    # declare the return variable
    result: Response

    # obtain the token data
    try:
        token_data: dict[str, Any] = __jwt_data.get_token_data(service_url=request.url)
        result = jsonify(token_data)
    except Exception as e:
        result = Response(response=repr(e),
                          status=400)

    return result
