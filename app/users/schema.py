# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel

from app.schema import HTTP_400_Response
from app.schema import HTTP_401_Response
from app.schema import HTTP_403_Response
from app.schema import HTTP_404_Response


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


class HTTP_201_Response(BaseModel):
    id: int


class UserProfile(BaseModel):
    pass
