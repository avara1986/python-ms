# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import datetime
import uuid

from flask_login import UserMixin
from project.models import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator, CHAR


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class ConfigModel(object):
    idpublic = Column(GUID, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.datetime.now)


class User(db.Model, ConfigModel, UserMixin):
    __tablename__ = 'auth_user'
    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, default="")
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, username, password):
        from project import bcrypt
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, 13
        ).decode()
