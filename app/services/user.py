from ..models.user import Users
import bson
from .auth import HashingMixin


class UserService:
    @staticmethod
    def user_exists(email: str) -> bool:
        num_users = Users.objects(email=email).count()
        return num_users > 0

    @staticmethod
    def get_user(email: str) -> Users:
        user = Users.objects(email=email).first()
        return user

    @staticmethod
    def get_user_by_id(id: str) -> Users:
        user = Users.objects(id=bson.ObjectId(id)).first()
        return user

    @staticmethod
    def delete_user(user: Users) -> bool:
        try:
            user.delete()
            return True
        except Exception:
            return False

    @staticmethod
    def update_password(user: Users, new_password: str) -> bool:
        hashed_password = HashingMixin.hash(new_password)
        user.password = hashed_password
        try:
            user.save()
            return True
        except Exception:
            return False
