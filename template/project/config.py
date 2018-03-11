# coding=utf-8
from __future__ import unicode_literals, print_function

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    DEBUG = False
    TESTING = False
    APP_NAME = "Template"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "gjr39dkjn344_!67#"


class DevConfig(Config):
    DEBUG = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db.sqlite3'.format(os.path.dirname(BASE_DIR))
    OAUTH_SERVER = "http://localhost:8000/protected"


class PreConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db.sqlite3'.format(os.path.dirname(BASE_DIR))
    OAUTH_SERVER = "http://oauth:5000/protected"


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, "prod.db")
    OAUTH_SERVER = "http://oauth:5000/protected"


config = {
    "dev": DevConfig,
    "pre": PreConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
