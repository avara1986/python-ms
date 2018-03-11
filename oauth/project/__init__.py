# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import os
from flasgger import Swagger
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from project.config import config
from project.models.models import User
from cmreslogging.handlers import CMRESHandler

"""
class LoggerConfig:
    dictConfig = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {'format': '%(asctime)s - %(name)s - %(levelname)s - '
                                   '%(message)s - [in %(pathname)s:%(lineno)d]'},
            'short': {'format': '%(message)s'}
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'app.log',
                'maxBytes': 5000000,
                'backupCount': 10
            },
            'debug': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG'
            },
            'elasticsearch': {
                'level': 'DEBUG',
                'class': 'cmreslogging.handlers.CMRESHandler',
                'hosts': [{'host': '192.168.99.100', 'port': 9200}],
                'es_index_name': 'my_python_app',
                'es_additional_fields': {'App': 'Test', 'Environment': 'Dev'},
                'auth_type': CMRESHandler.AuthType.NO_AUTH,
                'use_ssl': False,
            },
        },
        'loggers': {
            'project': {
                'handlers': ['default', "elasticsearch"],
                'level': 'DEBUG',
                'propagate': True
            },
            'project2': {
                'handlers': ['default', "elasticsearch"],
                'level': 'DEBUG',
                'propagate': True
            },
            'werkzeug': {'handlers': ['default'], 'propagate': True},
        },
        # 'root': {'level': 'DEBUG', 'handlers': ["console", "default"]}
    }
"""

ENVIRONMENT = os.environ.get("ENVIRONMENT", "default")

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
    app.config.from_object(config[ENVIRONMENT])

    if not app.config["DEBUG"]:
        handler = CMRESHandler(hosts=[{'host': '192.168.99.100', 'port': 9200}],
                               auth_type=CMRESHandler.AuthType.NO_AUTH,
                               es_index_name="my_python_index",
                               es_additional_fields={'App': app.config["APP_NAME"], 'Environment': ENVIRONMENT})

        app.logger.addHandler(handler)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWT(app, authenticate, identity)
    swagger = Swagger(app, config=swagger_config)

    app.register_blueprint(views_blueprint)
    return app, db
