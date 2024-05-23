# -*- coding: utf-8 -*-

import config

from sqlalchemy import select

from app.db import db
from app.models import User


def fill_database_by_initial_values():

    with db.Session() as session:
        superuser = session.execute(
            select(User).filter_by(email=config.SUPERUSER_EMAIL)
        ).scalar_one_or_none()

    if superuser is None:
        superuser = User()

    superuser.email = config.SUPERUSER_EMAIL
    superuser.set_password(config.SUPERUSER_PASSWORD)
    superuser.name = config.SUPERUSER_NAME
    superuser.is_superuser = True
    superuser.is_admin = True

    with db.Session() as session:
        session.add(superuser)
        session.commit()
