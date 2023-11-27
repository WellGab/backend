from fastapi.testclient import TestClient
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
import pytest

from app.services.user import UserService
from app.services.validation_token import ValidationTokenService
from app.models.validation_token import TokenTypeEnum
from app.utils.setup import config as cg
from app.main import app


client = TestClient(app)

class TestConfig(BaseSettings):
    username: str = "user-test@gmail.com"
    password: str = "1235678904"

    model_config = SettingsConfigDict(
        env_prefix="MYAPI_TEST_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

_config = TestConfig()


@pytest.fixture
def config():
    return _config


@pytest.fixture
def headers():
    data = {
        "username": _config.username,
        "password": _config.password,
    }

    response = client.post(f'{cg.ROOT_PATH}{cg.AUTH_URL}/token', data=data)
    schema = response.json()

    return {"Authorization": "Bearer " + schema["access_token"]}

@pytest.fixture
def password_reset_token() -> str:
    user = UserService.get_user(_config.username)
    validated_token = ValidationTokenService.create_token(user, TokenTypeEnum.PASSWORDRESET)
    return validated_token.token