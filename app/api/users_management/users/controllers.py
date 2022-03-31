from flask import request
from flask_accepts import for_swagger
from flask_restx import Namespace, Resource, marshal
from injector import inject
from marshmallow.exceptions import ValidationError

from app.api.commons.commons import error_response
from app.api.users_management.users.schemas import (
    ErrorSchema,
    GetUsersResponseSchema,
    UsersSchema,
)
from .services import UserService

user_ns = Namespace("user", description="User management operations")
users_ns = Namespace("users", description="Users management operations")


class ControllerInjector(Resource):
    @inject
    def __init__(self, service: UserService, **kwargs):
        self.service = service
        self.api = kwargs["api"]


@users_ns.route("/")
class GetUsers(ControllerInjector):
    @user_ns.marshal_with(
        fields=for_swagger(GetUsersResponseSchema, api=users_ns, operation="dump"),
        code=200,
        as_list=False,
    )
    def get(self):
        """Return all users"""
        return self.service.get_users()


@user_ns.route("/")
class GetUsers(ControllerInjector):
    @user_ns.expect(for_swagger(schema=UsersSchema, api=user_ns, operation="load"))
    @user_ns.response(
        code=201,
        description="User data successfully sent",
    )
    @user_ns.response(
        code=400,
        description="Bad Request",
        model=for_swagger(schema=ErrorSchema, api=user_ns, operation="dump"),
    )
    def post(self):
        """Create a new User"""
        try:
            schema = UsersSchema()
            user = schema.load(request.json)
            response = self.service.create_user(user)
            return marshal(response, for_swagger(schema=UsersSchema, api=user_ns)), 201
        except ValidationError as validation_error:
            return error_response(
                "E01",
                validation_error.messages,
                "Fields Validation Error",
                "/users_management/users/",
                400,
            )


@user_ns.route("/<string:name>")
class GetUserByName(ControllerInjector):
    @user_ns.response(
        code=200, description="", model=for_swagger(schema=UsersSchema, api=user_ns)
    )
    @user_ns.response(
        code=400,
        description="Bad Request",
        model=for_swagger(schema=ErrorSchema, api=user_ns),
    )
    def get(self, name: str):
        """Get a specific user data by their username"""
        try:
            response = self.service.get_user_data(name)
            return (
                marshal(response, fields=for_swagger(schema=UsersSchema, api=user_ns)),
                200,
            )
        except ValueError:
            return error_response(
                "E002",
                {"param": f"{name} Not found"},
                "User not found",
                "/users_management/users/",
                404,
            )
