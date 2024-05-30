# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel


class Department(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class User(BaseModel):
    id: int
    name: Optional[str] = None
    department: Department


class UserFilters(BaseModel):
    name: Optional[str] = None
    birthdate_from: Optional[date] = None
    birthdate_to: Optional[date] = None
    department_id: Optional[int] = None


class CreateUserRequest(BaseModel):
    email: str
    password: str
    is_admin: Optional[bool] = False
    name: str
    birthdate: Optional[date] = None


class CreateUserResponse(BaseModel):
    id: int
