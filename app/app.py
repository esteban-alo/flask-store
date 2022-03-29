from flask import Flask, jsonify
from flask_injector import FlaskInjector
from marshmallow import ValidationError

from .api.users_management.blueprints.user_management import (
    blueprint as users_management,
)

from .api.users_management.users.dependencies import (
    configure as user_configure
)

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True



app.register_blueprint(users_management)

FlaskInjector(
    app=app,
    modules=[
        user_configure
    ]
)