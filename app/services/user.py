from ..models.user import User


class UserService:
    @staticmethod
    def user_exists(email: str) -> bool:
        num_users = User.objects(email=email).count()
        return num_users > 0

    @staticmethod
    def get_user(email: str) -> User:
        user = User.objects(email=email).first()
        return user
