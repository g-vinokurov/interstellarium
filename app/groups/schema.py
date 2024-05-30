# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


class Group(BaseModel):
    id: int
    name: Optional[str] = None


class GroupFilters(BaseModel):
    name: Optional[str] = None


class CreateGroupRequest(BaseModel):
    name: str


class CreateGroupResponse(BaseModel):
    id: int
