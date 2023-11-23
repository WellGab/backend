from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .config import Configuration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

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