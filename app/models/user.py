from .base import BaseModel
from .fields import StringField, EmailField, UUIDField
import uuid


class User(BaseModel):
    _id = StringField(required=False)
    firstname = StringField(required=False)
    lastname = StringField(required=False)
    email = EmailField(unique=True, required=False)
    password = StringField(required=False)
