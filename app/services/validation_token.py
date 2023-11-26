from ..models.validation_token import ValidationToken, TokenTypeEnum
from ..models.user import Users
import bson
import random
from datetime import datetime


class ValidationTokenService:
    @staticmethod
    def create_token(user: Users, token_type: TokenTypeEnum, expiry: datetime = None) -> ValidationToken:
        random_number = random.randrange(100000, 1000000)
        random_string = str(random_number)

        token:  ValidationToken = ValidationToken(
            user=user,
            type=token_type,
            token=random_string,
        )

        if expiry:
            token.expiry = expiry

        token.save()
        return token

    @staticmethod
    def get_token_with_type(user: Users, token: str, token_type: TokenTypeEnum) -> ValidationToken:
        validation_token = ValidationToken.objects(
            token=token, type=token_type, user=user).first()
        return validation_token

    @staticmethod
    def get_token(user: Users, token: str) -> ValidationToken:
        validation_token = ValidationToken.objects(
            token=token, user=user).first()
        return validation_token

    @staticmethod
    def get_token_by_id(id: str) -> ValidationToken:
        validation_token = ValidationToken.objects(
            id=bson.ObjectId(id)).first()
        return validation_token

    @staticmethod
    def delete_token(token: ValidationToken) -> bool:
        try:
            token.delete()
            return True
        except Exception:
            return False
