# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: Optional[str] = None
    birthdate: Optional[date] = None


class UserFilters(BaseModel):
    name: Optional[str] = None
    birthdate_from: Optional[date] = None
    birthdate_to: Optional[date] = None
    department_id: Optional[int] = None
