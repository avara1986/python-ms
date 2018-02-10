# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import os

from flasgger import Swagger
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from project.config import config
from project.models.models import User

bcrypt = Bcrypt()

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "securityDefinitions": {
        "APIKeyHeader": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "uiversion": 2,
    "specs_route": "/apidocs/"
}


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(
            user.password, password
    ):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


def create_app():
    from project.models import db
    from project.views import views_bp as views_blueprint

    app = Flask(__name__)
    app.config.from_object(config[os.environ.get("ENVIRONMENT", "default")])
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWT(app, authenticate, identity)
    swagger = Swagger(app, config=swagger_config)

    app.register_blueprint(views_blueprint)
    return app, db
