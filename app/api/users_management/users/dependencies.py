from injector import singleton

from .services import UserService


def configure(binder):
    binder.bind(UserService, to=UserService, scope=singleton)
