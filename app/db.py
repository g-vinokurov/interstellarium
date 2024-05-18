# -*- coding: utf-8 -*-

import sqlalchemy
import sqlalchemy.orm as orm

from sqlalchemy.engine import Engine
from sqlalchemy import event

from . import models

import config


# You have to use Foreign Keys Support for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Database:
    def __init__(self):
        engine = sqlalchemy.create_engine(
            url=config.DB_URL,
            echo=config.DB_ECHO
        )
        self.Session = orm.sessionmaker(bind=engine)
        models.Base.metadata.create_all(engine)
