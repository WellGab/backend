from mongoengine import *
from datetime import datetime


class Conversations(Document):
    uid = ObjectIdField(required=True)
    message = StringField(required=True)
    reply = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())