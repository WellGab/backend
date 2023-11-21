from .base import (
    BaseService,
    BaseDataManager
)

class HashingMixin:
    """Hashing and verifying passwords."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Generate a bcrypt hashed password."""
        
        return password

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verify a password against a hash."""

        return False

class AuthService(HashingMixin, BaseService):
    """Authentication service."""

    def create_user(self) -> None:
        """Add user with hashed password to database."""

        AuthDataManager(self.session).add_user()

    def login_user(self) -> None:
        """Verifies login credentials and returns access token."""

class AuthDataManager(BaseDataManager):
    def add_user(self) -> None:
        """Write user to database."""

        self.add_one({})

    def get_user(self, email: str) -> None:
        """Read user from database."""