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


class User(BaseModel):
    id: int
    email: str
    is_superuser: bool
    is_admin: bool


class LoginResponse(BaseModel):
    token: Token
    user: User
