from app.api.commons.commons import uuid
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import Any, List


@dataclass_json
@dataclass
class User:
    id: int = None
    created_at: str = str(datetime.now())
    email: str = None
    name: str = None
    updated_at: str = str(datetime.now())
    uuid: str = uuid()


@dataclass
class PaginatedResults:
    limit: int
    offset: int
    total: int


@dataclass_json
@dataclass
class UsersResponse(PaginatedResults):
    results: List[User]

    def obj_dict(self):
        return self.__dict__


@dataclass_json
@dataclass
class ErrorResponse:
    details: dict
    error: str
    message: str
    path: str
    status: int
    timestamp: datetime
