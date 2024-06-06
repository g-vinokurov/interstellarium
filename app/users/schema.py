# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse


class Department(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class User(BaseModel):
    id: int
    name: Optional[str] = None
    department: Department


class CreateUserRequest(BaseModel):
    email: str
    password: str
    is_admin: Optional[bool] = False
    name: str
    birthdate: Optional[date] = None


class UserProfile(BaseModel):
    pass
