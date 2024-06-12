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

from app.schema import ID


class Group(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Project(BaseModel):
    id: Optional[int] = None
    name: Optional[int] = None


class Contract(BaseModel):
    id: Optional[int] = None
    name: Optional[int] = None


class ProjectAssignment(BaseModel):
    id: Optional[int] = None
    assignment_date: Optional[str] = None
    is_assigned: Optional[bool] = None
    project: Project


class ContractAssignment(BaseModel):
    id: Optional[int] = None
    assignment_date: Optional[str] = None
    is_assigned: Optional[bool] = None
    contract: Contract


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
    id: int
    name: Optional[str] = None
    birthdate: Optional[str] = None
    is_admin: Optional[bool] = None
    department: Department
    groups: list[Group]
    projects_assignments: list[ProjectAssignment]
    contracts_assignments: list[ContractAssignment]
