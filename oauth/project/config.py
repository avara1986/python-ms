# coding=utf-8
from __future__ import unicode_literals, print_function

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    APP_NAME = "Oauth"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "gjr39dkjn344_!67#"


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db.sqlite3'.format(os.path.dirname(BASE_DIR))


class PreConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, "prod.db")


class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, "prod.db")


config = {
    "dev": DevConfig,
    "pre": PreConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
