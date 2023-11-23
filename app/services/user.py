from ..models.user import User

class UserService:
    def user_exists(self, email: str) -> bool:
        num_users = User.objects(email=email).count()
        return num_users > 0
    

    def get_user(self, email: str) -> User:
        user = User.objects(email=email).first()
        return user