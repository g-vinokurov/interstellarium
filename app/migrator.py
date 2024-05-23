# -*- coding: utf-8 -*-

import config


class Migrator:
    def __init__(self, url, echo, migrations):

        # session = db.Session()

        # email = config.SUPERUSER_EMAIL
        # password = config.SUPERUSER_PASSWORD
        # name = config.SUPERUSER_NAME

        # user = session.query(User).filter_by(email=email).first()

        # if user is None:
        #     user = User()

        # user.email = email
        # user.set_password(password)
        # user.name = name
        # user.is_superuser = True
        # user.is_admin = True

        # session.add(user)
        # session.commit()
        pass


migrator = Migrator(config.DB_URL, config.DB_ECHO, config.DB_MIGRATIONS)
