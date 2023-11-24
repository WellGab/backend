from ..models.user import Users


class UserService:
    @staticmethod
    def user_exists(email: str) -> bool:
        num_users = Users.objects(email=email).count()
        return num_users > 0

    @staticmethod
    def get_user(email: str) -> Users:
        user = Users.objects(email=email).first()
        return user
