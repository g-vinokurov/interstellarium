# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


class Contract(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Project(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Work(BaseModel):
    id: int
    name: Optional[str] = None
    cost: float = 0.0
    contract: Contract
    project: Project


class WorkFilters(BaseModel):
    name: Optional[str] = None
    min_cost: Optional[float] = None
    max_cost: Optional[float] = None


class CreateWorkRequest(BaseModel):
    name: str
    cost: float = 0.0


class CreateWorkResponse(BaseModel):
    id: int
