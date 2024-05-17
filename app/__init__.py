# -*- coding: utf-8 -*-

from flask import Flask

from flask_wtf.csrf import CSRFProtect

import config

app = Flask(
    import_name=__name__,
    template_folder=config.FLASK_TEMPLATES,
    static_folder=config.FLASK_STATIC
)

app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

csrf_protection = CSRFProtect()
csrf_protection.init_app(app)

from . import db
from . import forms
from . import views


def run():
    host = config.FLASK_HOST
    port = config.FLASK_PORT
    app.run(host, port)
