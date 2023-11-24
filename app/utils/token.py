from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import json
from urllib.request import urlopen
from datetime import datetime, timedelta

from .config import Configuration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

class Auth0Error(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

class Token():
    def __init__(self, config: Configuration):
            self.config = config

    def create_access_token(self, payload: dict) -> str:
        to_encode = payload.copy()

        expire = datetime.utcnow() + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)

        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception) -> str:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])

            id: str = payload.get("user_id")

            if id is None: 
                raise credentials_exception

        except JWTError as error:
            print("Error: ", error)
            raise credentials_exception

        return id
    
    def verify_social_auth_token(self, token: str) -> dict:
        jsonurl = urlopen(f'https://{self.config.AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        print(unverified_header)
        rsa_key = {}
        if 'kid' not in unverified_header:
            raise Auth0Error({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.config.AUTH0_ALGORITHMS,
                    audience=self.config.API_AUDIENCE,
                    issuer='https://' + self.config.AUTH0_DOMAIN + '/'
                )
                email = payload['email']
                if email == '' or not email:
                    return None

                return {
                    'email': email,
                    'sub': payload['sub']
                }

            except jwt.ExpiredSignatureError:
                raise Auth0Error({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

            except jwt.JWTClaimsError:
                raise Auth0Error({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception:
                raise Auth0Error({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        raise Auth0Error({
                    'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
                }, 400)