# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse
from app.schema import OkResponse


class UserID(BaseModel):
    id: Optional[int] = None


class WorkID(BaseModel):
    id: Optional[int] = None


class ContractID(BaseModel):
    id: Optional[int] = None


class ProjectID(BaseModel):
    id: Optional[int] = None


class EquipmentID(BaseModel):
    id: Optional[int] = None


class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Work(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    cost: Optional[float] = 0.0


class Contract(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Project(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Equipment(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Group(BaseModel):
    id: int
    name: Optional[str] = None


class CreateGroupRequest(BaseModel):
    name: str


class GroupProfile(BaseModel):
    id: int
    name: Optional[str] = None
    users: list[User]
    works: list[Work]
    contracts: list[Contract]
    projects: list[Project]
    equipment: list[Equipment]
