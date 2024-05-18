# -*- coding: utf-8 -*-

import sqlalchemy
import sqlalchemy.orm as orm

from . import models

import config


class Database:
    def __init__(self):
        engine = sqlalchemy.create_engine(
            url=config.DB_URL,
            echo=config.DB_ECHO
        )
        self.Session = orm.sessionmaker(bind=engine)
        models.Base.metadata.create_all(engine)
