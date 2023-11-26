
from mongoengine import *
from datetime import datetime, timedelta
from .user import Users
from enum import Enum


class TokenTypeEnum(Enum):
    PASSWORDRESET = "password_reset"


class ValidationToken(Document):
    user = ReferenceField(Users, required=True)
    token = StringField(required=True)
    type = EnumField(TokenTypeEnum, required=True)
    expiry = DateTimeField(default=datetime.now() + timedelta(hours=2))
    created_at = DateTimeField(default=datetime.now())

    meta = {
        'indexes': [
            {
                'fields': ['expiry'],
                'expireAfterSeconds': 0  # Set to 0 for background deletion during expiry
            }
        ]
    }
