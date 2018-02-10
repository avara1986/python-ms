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


class Colors(db.Model, ConfigModel, UserMixin):
    __tablename__ = 'colors'
    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
