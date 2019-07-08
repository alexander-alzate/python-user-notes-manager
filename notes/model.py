"""User model definition module"""

import datetime
from mongoengine import Document, DateTimeField, StringField
from flask_restful import fields

NOTE_FIELDS = {
    "id": fields.String,
    "uid": fields.String,
    "subject": fields.String,
    "createdAt": fields.DateTime,
    "body": fields.String,
}

class NoteModel(Document):
    """User data model"""
    # QSTN: Is there a way to make custom validations?
    uid = StringField(required=True)
    subject = StringField(required=True, max_length=32)
    createdAt = DateTimeField(default=datetime.datetime.now())
    body = StringField(required=True, max_length=512)
