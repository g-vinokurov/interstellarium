# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse
from app.schema import OkResponse


class UserID(BaseModel):
    id: Optional[int] = None


class GroupID(BaseModel):
    id: Optional[int] = None


class Chief(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Group(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Project(BaseModel):
    id: int
    name: Optional[str] = None


class Work(BaseModel):
    id: int
    name: Optional[str] = None
    cost: float = 0.0


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
    id: int
    name: Optional[str] = None
    start_date: Optional[str] = None
    finish_date: Optional[str] = None
    chief: Chief
    group: Group
    projects: list[Project]
    works: list[Work]
