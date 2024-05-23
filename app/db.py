# -*- coding: utf-8 -*-

import config

import sqlalchemy
import sqlalchemy.orm as orm

from . import models


class Database:
    def __init__(self, url, echo):
        engine = sqlalchemy.create_engine(url=url, echo=echo)
        self.Session = orm.sessionmaker(bind=engine)
        models.Base.metadata.create_all(engine)

    def get(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()


db = Database(url=config.DB_URL, echo=config.DB_ECHO)
