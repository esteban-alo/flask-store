from flask import request
from flask_accepts import for_swagger
from flask_restx import Namespace, Resource
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
    @api.marshal_with(fields=for_swagger(UsersSchema, api=api, operation="dump"), code=201, as_list=False)
    @api.response(code=400, description="Bad Request", model=for_swagger(schema=ErrorSchema, api=api, operation="dump"))
    def post(self):
        """ Create a new User """
        try:
            schema = UsersSchema()
            user = schema.load(request.json)
            return self.service.create_user(user), 201
        except Exception as validation_error:
            return error_response("E01", validation_error.messages, "Fields Validation Error",
                                  "/users_management/users/", 400)


@api.route("/<string:name>")
class GetUserByName(Resource):

    @inject
    def __init__(self, service: UserService, **kwargs):
        self.service = service
        self.api = kwargs["api"]

    @api.marshal_with(fields=for_swagger(UsersSchema, api=api, operation="dump"), code=200, as_list=False)
    @api.response(code=400, description="Bad Request", model=for_swagger(schema=ErrorSchema, api=api, operation="dump"))
    def get(self, name: str):
        """ Get a specific user data by their username """
        return self.service.get_user_data(name)
