# -*- coding: utf-8 -*-

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    msg: str


class BadRequestError(ErrorResponse):
    pass


class UnauthorizedError(ErrorResponse):
    pass


class ForbiddenError(ErrorResponse):
    pass


class NotFoundError(ErrorResponse):
    pass


class CreatedResponse(BaseModel):
    id: int
