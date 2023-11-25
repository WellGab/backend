from ..models.user import Users
import bson


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
