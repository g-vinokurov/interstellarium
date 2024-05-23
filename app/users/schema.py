# -*- coding: utf-8 -*-

from pydantic import BaseModel


class User(BaseModel):
    email: str
