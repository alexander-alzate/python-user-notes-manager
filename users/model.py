"""User model definition module"""

import datetime
from mongoengine import Document, EmailField, DateTimeField, StringField
from flask_restful import fields

USER_FIELDS = {
    "id": fields.String,
    "email": fields.String,
    "createdAt": fields.DateTime,
    "name": fields.String,
    "lastName": fields.String,
    "birth": fields.DateTime,
    "sex": fields.String
}

class UserModel(Document):
    """User data model"""
    email = EmailField(unique=True, required=True)
    createdAt = DateTimeField(default=datetime.datetime.now())
    name = StringField(required=True, max_length=32)
    lastName = StringField(required=True)
    birth = DateTimeField(required=True)
    sex = StringField(required=True, choices=['male', 'female', 'other'])
