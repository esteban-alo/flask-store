from typing import List

from injector import inject

from app.api.commons.commons import (
    get_current_datetime,
    uuid,
)
from app.api.users_management.users.interfaces import (
    User,
    UsersResponse,
)


class UserService:
    id: int
    users_list: List[User]

    @inject
    def __init__(self):
        self.id = 0
        self.users_list = []

    def create_user(self, user: User) -> dict:
        """Get users data by username"""
        user_schema = User.schema()
        user.id = self.id
        user.uuid = uuid()
        user.created_at = get_current_datetime()
        user.updated_at = get_current_datetime()
        self.id = self.id + 1
        self.users_list.append(user)
        return user_schema.dump(user)

    def get_users(self):
        response = UsersResponse.schema()
        result = UsersResponse(
            limit=0, offset=0, total=len(self.users_list), results=self.users_list
        )
        return response.dump(result)

    def get_user_data(self, name: str) -> dict:
        """Get users data by username"""
        user_schema = User.schema()
        for item in self.users_list:
            if item.name.lower() == name.lower():
                return user_schema.dump(item)
        raise ValueError
