from injector import singleton

from app.api.users_management.users.services import UserService


def configure(binder):
    binder.bind(UserService, to=UserService, scope=singleton)
