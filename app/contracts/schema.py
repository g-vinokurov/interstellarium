# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse


class Chief(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Group(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Contract(BaseModel):
    id: int
    name: Optional[str] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None
    chief: Chief
    group: Group


class CreateContractRequest(BaseModel):
    name: str
    start_date: Optional[date] = None
    finish_date: Optional[date] = None


class ContractProfile(BaseModel):
    pass
