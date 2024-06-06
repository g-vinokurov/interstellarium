# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse


class Chief(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Department(BaseModel):
    id: int
    name: Optional[str] = None
    chief: Chief


class CreateDepartmentRequest(BaseModel):
    name: str


class DepartmentProfile(BaseModel):
    pass
