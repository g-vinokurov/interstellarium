# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel


class MsgResponse(BaseModel):
    msg: str


class OkResponse(MsgResponse):
    pass


class CreatedResponse(BaseModel):
    id: int


class BadRequestError(MsgResponse):
    pass


class UnauthorizedError(MsgResponse):
    pass


class ForbiddenError(MsgResponse):
    pass


class NotFoundError(MsgResponse):
    pass
