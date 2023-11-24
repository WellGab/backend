from fastapi.testclient import TestClient
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
import pytest

from app.utils.setup import config
from app.main import app


client = TestClient(app)


class TestConfig(BaseSettings):
    username: str = ""
    password: str = ""

    model_config = SettingsConfigDict(
        env_prefix="MYAPI_TEST_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


_config = TestConfig()

@pytest.fixture
def config():
    return _config