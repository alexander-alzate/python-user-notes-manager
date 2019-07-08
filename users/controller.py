"""Controller code module"""

import json
from flask import Request
from flask_restful import Resource, marshal_with
from injector import inject

from model import USER_FIELDS
from service import UserService

DEFAULT_PAGE_SIZE = 20

class UserList(Resource):
    """User Resource: The API for multiple user requests"""
    @inject
    def __init__(self, user_request: Request, user_service: UserService):
        self._request = user_request
        self._user_service = user_service

    @marshal_with(USER_FIELDS)
    def get(self):
        """GET HTTP method manager"""
        query = json.loads(self._request.args.get('query', '{}'))
        page = int(self._request.args.get('page', 0))
        page_size = int(self._request.args.get('page_size', DEFAULT_PAGE_SIZE))

        return self._user_service.find_all(page, page_size, **query)

    @marshal_with(USER_FIELDS)
    def post(self):
        """POST HTTP method manager: Creates new users"""
        user_data = self._request.get_json(force=True)

        # TODO: handle validation errors
        if user_data is not None:
            new_user = self._user_service.create_new(**user_data)
            new_user.save()
            new_user.reload()

            return new_user

        # FIXME: throw an HTTP error
        return None

class User(Resource):
    """User Resource: The API for single user requests"""
    @inject
    def __init__(self, user_request: Request, user_service: UserService):
        self._request = user_request
        self._user_service = user_service

    @marshal_with(USER_FIELDS)
    def get(self, uid):
        """GET HTTP method manager"""
        return self._load_model(uid)

    @marshal_with(USER_FIELDS)
    def put(self, uid):
        """PUT HTTP method manager"""
        user_data = self._request.get_json(force=True)
        user = self._load_model(uid)

        for attribute in user_data:
            user[attribute] = user_data[attribute]

        user.save()

        return user

    @marshal_with(USER_FIELDS)
    def delete(self, uid):
        """DELETE HTTP method manager"""
        user = self._load_model(uid)
        user.delete()

        return user

    def _load_model(self, uid):
        """Loads the user identified by the given id"""
        return self._user_service.find(pk=uid)
