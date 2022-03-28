from flask import Blueprint
from flask_restx import Api
from app.api.users_management.users.controllers import api as users_management_ns

blueprint = Blueprint('users_bp', __name__, static_folder='static',
                      static_url_path='icons', url_prefix='/users_management')

api = Api(blueprint, version="1.0", title="User management")
api.add_namespace(users_management_ns)
