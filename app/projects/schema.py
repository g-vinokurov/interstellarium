# -*- coding: utf-8 -*-

from typing import Optional

from datetime import date
from pydantic import BaseModel


class Chief(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Group(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Project(BaseModel):
    id: int
    name: Optional[str] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None
    chief: Chief
    group: Group


class ProjectFilters(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    finish_date: Optional[date] = None


class CreateProjectRequest(BaseModel):
    name: str
    start_date: Optional[date] = None
    finish_date: Optional[date] = None


class CreateProjectResponse(BaseModel):
    id: int
