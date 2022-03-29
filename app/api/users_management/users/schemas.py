from marshmallow import (
    Schema,
    fields,
    post_load
)

from .interfaces import User


class ErrorSchema(Schema):
    details = fields.Dict()
    error = fields.Str()
    message = fields.Str()
    path = fields.Url()
    timestamp = fields.Str()
    status = fields.Int()

    class Meta:
        ordered = True


class UsersSchema(Schema):
    """User Schema"""

    id = fields.Int()
    created_at = fields.Str()
    email = fields.Email(required=True)
    name = fields.String(required=True)
    updated_at = fields.Str()
    uuid = fields.UUID()

    class Meta:
        dump_only = ("created_at", "updated_at", "uuid",)
        exclude = ("id",)

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
    results = fields.List(fields.Nested(UsersSchema))
