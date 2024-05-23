# -*- coding: utf-8 -*-

import dotenv
import os

env = dotenv.dotenv_values('.env')

# Project config
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data source name url for db connection
DB_URL = env.get('DB_URL', '')
DB_ECHO = (env.get('DB_ECHO', 'False') == 'True')
DB_MIGRATIONS = os.path.join(PROJECT_DIR, env.get('DB_MIGRATIONS', ''))

# JWT-auth config
AUTH_SECRET_KEY = env.get('AUTH_SECRET_KEY', 'a secret key')
AUTH_ALGORITHM = env.get('AUTH_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

# Superuser config
SUPERUSER_EMAIL = env['SUPERUSER_EMAIL']
SUPERUSER_PASSWORD = env['SUPERUSER_PASSWORD']
SUPERUSER_NAME = env['SUPERUSER_NAME']
SUPERUSER_BIRTHDATE = env['SUPERUSER_BIRTHDATE']
