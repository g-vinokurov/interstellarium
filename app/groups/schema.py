# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel

from app.schema import BadRequestError
from app.schema import UnauthorizedError
from app.schema import ForbiddenError
from app.schema import NotFoundError
from app.schema import CreatedResponse


class Group(BaseModel):
    id: int
    name: Optional[str] = None


class CreateGroupRequest(BaseModel):
    name: str


class GroupProfile(BaseModel):
    pass
