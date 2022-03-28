import json
from injector import inject
from .interfaces import (
    User,
    UsersResponse,
)
from app.api.commons.commons import error_response
from .schemas import ErrorSchema


class UserService:
    users_list: list[User]

    @inject
    def __init__(self):
        self.users_list = []

    def create_user(self, user: User) -> None:
        """ Get users data by username """
        self.users_list.append(user)

    def get_users(self):
        paginated_result = {
            "limit": 0,
            "offset": 0,
            "total": len(self.users_list),
            "results": json.loads(json.dumps(self.users_list, default=lambda x: x.__dict__))
        }
        return paginated_result

    def get_user_data(self, name: str) -> User:
        """ Get users data by username """
        for user in self.users_list:
            return user.to_dict()
        return error_response("E01", f"{name} object not Found", "Fields Validation Error",
                               "/users_management/users/", 404)

