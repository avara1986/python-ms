# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
import os

from flasgger import Swagger
from flask import Flask
from project.config import config
from cmreslogging.handlers import CMRESHandler

ENVIRONMENT = os.environ.get("ENVIRONMENT", "default")

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
    swagger = Swagger(app, config=swagger_config)

    app.register_blueprint(views_blueprint)
    return app, db
