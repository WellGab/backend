from mongoengine import *
from datetime import datetime

AUTH_CHANNEL_DEFAULT = "email-and-password"
AUTH_CHANNEL_GOOGLE = "google"
AUTH_CHANNEL_APPLE = "apple"
AUTH_CHANNEL_MICROSOFT = "windows"

class Users(Document):
    firstname = StringField(required=False)
    lastname = StringField(required=False)
    username = StringField(required=False)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    auth_channel = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())
