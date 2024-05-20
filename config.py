# -*- coding: utf-8 -*-

import dotenv
import os

env = dotenv.dotenv_values('.env')

# Project config
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data source name url for db connection
DB_URL = env.get('DB_URL', '')
DB_ECHO = (env.get('DB_ECHO', 'False') == 'True')
