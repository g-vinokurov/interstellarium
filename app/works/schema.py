# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse


class Contract(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Project(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Executor(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Work(BaseModel):
    id: int
    name: Optional[str] = None
    cost: float = 0.0
    contract: Contract
    project: Project


class CreateWorkRequest(BaseModel):
    name: str
    cost: float = 0.0


class WorkProfile(BaseModel):
    id: int
    name: Optional[str] = None
    cost: float = 0.0
    contract: Contract
    project: Project
    executor: Executor
