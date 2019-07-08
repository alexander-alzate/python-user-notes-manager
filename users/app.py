"""User service"""

from flask import Flask, Request, request
from flask_injector import FlaskInjector
from flask_restful import Api

from controller import User, UserList
from service import UserService

API_VERSION = 'v1'

APP = Flask(__name__)
API = Api(APP)

API.add_resource(UserList, f'/{API_VERSION}/users/')
API.add_resource(User, f'/{API_VERSION}/users/<uid>')

def configure(binder):
    """Configures the injector"""
    binder.bind(
        UserService,
        to=UserService(),
        scope=request)
    binder.bind(
        Request,
        to=request,
        scope=request)

FlaskInjector(app=APP, modules=[configure])

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True)
