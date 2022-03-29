from dataclasses import dataclass, field
from typing import Any, Dict, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class User:
    id: int = field(init=False, repr=False)
    created_at: str = field(default_factory=str)
    email: str = field(default_factory=str, init=True)
    name: str = field(default_factory=str, init=True)
    updated_at: str = field(default_factory=str)
    uuid: str = field(default_factory=str)



@dataclass(order=True)
class PaginatedResults:
    limit: int
    offset: int
    total: int

@dataclass_json
@dataclass(order=True)
class UsersResponse(PaginatedResults):
    results: List[User] = field(default_factory=list, repr=True)


@dataclass_json
@dataclass(order=True)
class ErrorResponse:
    details: Dict[Any, Any]
    error: str
    message: str
    path: str
    status: int
    timestamp: str = field(default_factory=str)
