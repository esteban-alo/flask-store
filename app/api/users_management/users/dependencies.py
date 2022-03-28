from injector import singleton
from flask_injector import Binder, request

from .services import UserService


def configure(binder):
    binder.bind(UserService, to=UserService, scope=singleton)
