from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
import json
from urllib.request import urlopen
from datetime import datetime, timedelta

from .config import Configuration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Auth0Error(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class Token:
    def __init__(self, config: Configuration):
        self.config = config

    def create_access_token(self, payload: dict) -> str:
        to_encode = payload.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM
        )

        return encoded_jwt

    def verify_access_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM]
            )

            id: str = payload.get("user_id")
        except Exception:
            return None

        return id

    def verify_social_auth_token(self, token: str) -> dict:
        jsonurl = urlopen(f"https://{self.config.AUTH0_DOMAIN}/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        if "kid" not in unverified_header:
            raise Auth0Error(
                {"code": "invalid_header", "description": "Authorization malformed."},
                401,
            )

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.config.AUTH0_ALGORITHMS,
                    audience=self.config.API_AUDIENCE,
                    issuer="https://" + self.config.AUTH0_DOMAIN + "/",
                )
                email = payload.get("email")
                if email == "" or not email:
                    return {
                        "error": {
                            "message": "no_email",
                            "description": "No email address.",
                            "code": 403,
                        }
                    }

                return payload

            except jwt.ExpiredSignatureError:
                return {
                    "error": {
                        "message": "token_expired",
                        "description": "Token expired.",
                        "code": 401,
                    }
                }

            except jwt.JWTClaimsError:
                return {
                    "error": {
                        "message": "invalid_claims",
                        "description": "Incorrect claims. Please, check the audience and issuer.",
                        "code": 401,
                    }
                }
            except Exception as e:
                return {
                    "error": {
                        "message": "invalid_header",
                        "description": f"Unable to parse authentication token. {str(e)}",
                        "code": 400,
                    }
                }
        return {
            "error": {
                "message": "invalid_header",
                "description": "Unable to find the appropriate key.",
                "code": 400,
            }
        }
