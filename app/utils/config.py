from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from .const import SECRET_KEY, MONGO_URI, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class DatabaseConfig(BaseModel):
    """Backend database configuration parameters.

    Attributes:
        dsn:
            DSN for target database.
    """

    dsn: str = MONGO_URI

class Config(BaseSettings):
    """API configuration parameters.

    Automatically read modifications to the configuration parameters
    from environment variables and ``.env`` file.

    Attributes:
        database:
            Database configuration settings.
            Instance of :class:`app.util.config.DatabaseConfig`.
        secret_key:
            Random secret key used to sign JWT tokens.
        algorithm:
            Hashing algorithm.
        access_token_expiry:
            The token expiry time.
    """

    database: DatabaseConfig = DatabaseConfig()
    secret_key: str = SECRET_KEY
    algorithm: str = ALGORITHM
    access_token_expiry: int = ACCESS_TOKEN_EXPIRE_MINUTES

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MYAPI_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


config = Config()
