# -*- coding: utf-8 -*-

from flask import Flask

from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

import config

app = Flask(
    import_name=__name__,
    template_folder=config.FLASK_TEMPLATES,
    static_folder=config.FLASK_STATIC
)

app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

csrf_protection = CSRFProtect()
csrf_protection.init_app(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

from . import db as _db
from . import models

database = _db.Database()

from . import migrator as _migrator

migrator = _migrator.Migrator()
migrator.init()

from . import forms
from . import views


def run():
    host = config.FLASK_HOST
    port = config.FLASK_PORT
    app.run(host, port)
