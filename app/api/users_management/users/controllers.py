import json

from app.api.commons.commons import error_response
from .services import UserService
from .schemas import (
    ErrorSchema,
    GetUsersResponseSchema,
    UsersSchema,
)

from flask import request, jsonify
from flask_accepts import for_swagger
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow.exceptions import ValidationError

api = Namespace("users", description="User management operations")


@api.route("/")
class GetUsers(Resource):

    @inject
    def __init__(self, service: UserService, **kwargs):
        self.service = service
        self.api = kwargs["api"]

    @api.response(code=200, description="List of users", model=for_swagger(schema=GetUsersResponseSchema, api=api))
    def get(self):
        """ Return all users """
        return self.service.get_users()

    @api.expect(for_swagger(UsersSchema, api))
    @api.response(code=400, description="Bad Request", model=for_swagger(ErrorSchema, api))
    def post(self):
        """ Create a new User """
        try:
            schema = UsersSchema()
            user = schema.load(request.json)
            return self.service.create_user(user)
        except ValidationError as validation_error:
            return error_response("E01", validation_error.messages, "Fields Validation Error",
                                  "/users_management/users/", 400)


@api.route("/<string:name>")
class GetUserByName(Resource):

    @inject
    def __init__(self, service: UserService, **kwargs):
        self.service = service
        self.api = kwargs["api"]

    @api.response(code=200, description="", model=for_swagger(UsersSchema, api))
    @api.response(code=404, description="User Not Found", model=for_swagger(ErrorSchema, api))
    def get(self, name: str):
        """ Get a specific user data by their username """
        return self.service.get_user_data(name)
