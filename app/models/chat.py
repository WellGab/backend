from .user import Users
from mongoengine import *
from datetime import datetime


class Conversations(EmbeddedDocument):
    uid = ObjectIdField(required=True)
    user = ReferenceField(Users, required=True)
    message = StringField(required=True)
    reply = StringField()
    created_at = DateTimeField(default=datetime.now())


class Chats(Document):
    topic = StringField()
    user = ReferenceField(Users, required=True)
    conversations = ListField(EmbeddedDocumentField(Conversations))
    created_at = DateTimeField(default=datetime.now())


class AnonConversations(EmbeddedDocument):
    uid = ObjectIdField(required=True)
    anon_id = StringField()
    message = StringField(required=True)
    reply = StringField()
    created_at = DateTimeField(default=datetime.now())

class AnonChats(Document):
    topic = StringField()
    uid = StringField()
    conversations = ListField(EmbeddedDocumentField(AnonConversations))
    created_at = DateTimeField(default=datetime.now())
