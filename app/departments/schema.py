# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


class Chief(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Department(BaseModel):
    id: int
    name: Optional[str] = None
    chief: Chief


class DepartmentFilters(BaseModel):
    name: Optional[str] = None


class CreateDepartmentRequest(BaseModel):
    name: str


class CreateDepartmentResponse(BaseModel):
    id: int
