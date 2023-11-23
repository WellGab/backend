from mongoengine import *
from .base import BaseModel


class User(Document):
    # _id = StringField(required=False)
    firstname = StringField(required=False)
    lastname = StringField(required=False)
    username = StringField(required=False)
    email = EmailField(unique=True, required=False)
    password = StringField(required=False)
