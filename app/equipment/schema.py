# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse


class Department(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Group(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Equipment(BaseModel):
    id: int
    name: Optional[str] = None
    department: Department
    group: Group


class EquipmentFilters(BaseModel):
    name: Optional[str] = None


class CreateEquipmentRequest(BaseModel):
    name: str


class EquipmentProfile(BaseModel):
    pass
