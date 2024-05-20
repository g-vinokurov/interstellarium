# -*- coding: utf-8 -*-

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

import config


app = FastAPI()

# TODO: it must be confiured more carefully
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

from .migrator import Migrator
from .db import Database

migrator = Migrator(config.DB_URL, config.DB_ECHO, config.DB_MIGRATIONS)
db = Database(config.DB_URL, config.DB_ECHO)

from . import models


def run():
    pass
