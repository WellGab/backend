
from enum import Enum
from .user import Users
from mongoengine import *
from datetime import datetime


class SizeEnum(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class DisplayEnum(Enum):
    LIGHT = "light"
    DARK = "dark"


class Settings(Document):
    ninety_days_chat_limit = BooleanField(required=True, default=False)
    text_size = EnumField(SizeEnum, default=SizeEnum.MEDIUM)
    display = EnumField(DisplayEnum, default=DisplayEnum.LIGHT)
    user = ReferenceField(Users, required=True)
    created_at = DateTimeField(default=datetime.now())
