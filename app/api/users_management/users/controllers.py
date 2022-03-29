from flask import request
from flask_accepts import for_swagger
from flask_restx import Namespace, Resource, marshal
from injector import inject

from app.api.commons.commons import error_response
from .schemas import (
    ErrorSchema,
    GetUsersResponseSchema,
    UsersSchema,
)
from .services import UserService

api = Namespace("users", description="User management operations")


@api.route("/")
class GetUsers(Resource):

    @inject
    def __init__(self, service: UserService, **kwargs):
        self.service = service
        self.api = kwargs["api"]

    @api.marshal_with(fields=for_swagger(GetUsersResponseSchema, api=api, operation="dump"), code=200, as_list=False)
    def get(self):
        """ Return all users """
        return self.service.get_users()

    @api.expect(for_swagger(schema=UsersSchema, api=api, operation="load"))
    @api.response(code=201, description="User data successfully sent",)
    @api.response(code=400, description="Bad Request", model=for_swagger(schema=ErrorSchema, api=api, operation="dump"))
    def post(self):
        """ Create a new User """
        try:
            schema = UsersSchema()
            user = schema.load(request.json)
            response = self.service.create_user(user)
            return marshal(response, for_swagger(schema=UsersSchema, api=api)), 201
        except Exception as validation_error:
            return error_response("E01", validation_error.messages, "Fields Validation Error",
                                  "/users_management/users/", 400)


@api.route("/<string:name>")
class GetUserByName(Resource):

    @inject
    def __init__(self, service: UserService, **kwargs):
        self.service = service
        self.api = kwargs["api"]

    @api.response(code=200, description="", model=for_swagger(schema=UsersSchema, api=api))
    @api.response(code=400, description="Bad Request", model=for_swagger(schema=ErrorSchema, api=api))
    def get(self, name: str):
        """ Get a specific user data by their username """
        try:
            response = self.service.get_user_data(name)
            return marshal(response, fields=for_swagger(schema=UsersSchema, api=api)), 200
        except ValueError as value_error:
            return error_response("E002", {"param": f"{name} Not found"}, "User not found",
                                  "/users_management/users/", 404)
