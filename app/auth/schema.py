# -*- coding: utf-8 -*-

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class LoginRequest(BaseModel):
    email: str
    password: str
