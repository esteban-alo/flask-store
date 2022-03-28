from app.api.commons.commons import error_response
from .interfaces import User, ErrorResponse
from marshmallow import (
    Schema,
    fields,
    pre_load,
    pre_dump,
    post_dump,
    post_load,
    validate,
)

from marshmallow.exceptions import MarshmallowError


class AppError(MarshmallowError):
    pass


class ErrorSchema(Schema):
    details = fields.Dict()
    error = fields.Str()
    message = fields.Str()
    path = fields.Url()
    timestamp = fields.DateTime()
    status = fields.Int()

    class Meta:
        ordered = True


class UsersSchema(Schema):
    """User Schema"""

    class Meta:
        dump_only = ("created_at", "updated_at", "uuid",)
        exclude = ("id",)
        ordered = True

    id = fields.Int()
    created_at = fields.DateTime()
    email = fields.Email(required=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    updated_at = fields.DateTime()
    uuid = fields.UUID()

    @post_load
    def make(self, data, **kwargs):
        return User(**data)


class PaginatedResultsSchema(Schema):
    limit = fields.Int()
    offset = fields.Int()
    total = fields.Int()

    class Meta:
        ordered = True


class GetUsersResponseSchema(PaginatedResultsSchema):
    """Registered users list"""
    results = fields.Nested(UsersSchema, many=True)
