# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


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


class CreateEquipmentResponse(BaseModel):
    id: int
