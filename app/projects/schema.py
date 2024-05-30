# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int


class ProjectFilters(BaseModel):
    name: Optional[str] = None


class CreateProjectRequest(BaseModel):
    name: str


class CreateProjectResponse(BaseModel):
    id: int
