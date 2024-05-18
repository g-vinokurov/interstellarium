# -*- coding: utf-8 -*-

from app import database as db
from app.models import User

import config


class Migrator:
    def init(self):

        # Run manually all SQL-migrations before this step!

        session = db.Session()

        email = config.SUPERUSER_EMAIL
        password = config.SUPERUSER_PASSWORD
        name = config.SUPERUSER_NAME

        user = session.query(User).filter_by(email=email).first()
        if user is not None:
            return

        user = User()
        user.email = email
        user.set_password(password)
        user.name = name

        session.add(user)
        session.commit()
