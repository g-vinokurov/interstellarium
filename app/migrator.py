# -*- coding: utf-8 -*-

import config

from sqlalchemy import create_engine
from sqlalchemy.sql import text

import os


class Migrator:
    def __init__(self, url, echo, migrations):
        self.url = url
        self.echo = echo
        self.migrations = migrations

    def up(self):
        engine = create_engine(url=self.url, echo=self.echo)
        with engine.connect() as connection:
            self.__up(connection)
            connection.commit()

    def __up(self, connection):
        for filename in os.listdir(self.migrations):
            if not filename.endswith('.up.sql'):
                continue
            with open(os.path.join(self.migrations, filename)) as file:
                query = text(file.read())
            try:
                connection.execute(query)
            except Exception as error:
                print(error.with_traceback(None))


migrator = Migrator(config.DB_URL, config.DB_ECHO, config.DB_MIGRATIONS)
migrator.up()
