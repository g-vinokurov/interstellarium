# -*- coding: utf-8 -*-

import dotenv
import os

env = dotenv.dotenv_values('.env')

# Project config
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data source name url for db connection
DB_URL = env.get('DB_URL', '')
DB_ECHO = (env.get('DB_ECHO', 'False') == 'True')

# Flask application config
FLASK_SECRET_KEY = env.get('FLASK_SECRET_KEY', 'secret-key')
FLASK_HOST = env.get('FLASK_HOST', 'localhost')
FLASK_PORT = int(env.get('FLASK_PORT', 5000))

FLASK_TEMPLATES_DIR = env.get('FLASK_TEMPLATES_DIR', '')
FLASK_TEMPLATES = os.path.join(PROJECT_DIR, FLASK_TEMPLATES_DIR)

FLASK_STATIC_DIR = env.get('FLASK_STATIC_DIR', '')
FLASK_STATIC = os.path.join(PROJECT_DIR, FLASK_STATIC_DIR)

SUPERUSER_EMAIL = env.get('SUPERUSER_EMAIL', '')
SUPERUSER_PASSWORD = env.get('SUPERUSER_PASSWORD', '')
