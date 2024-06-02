# -*- coding: utf-8 -*-

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    msg: str


class HTTP_400_Response(ErrorResponse):
    pass


class HTTP_401_Response(ErrorResponse):
    pass


class HTTP_403_Response(ErrorResponse):
    pass


class HTTP_404_Response(ErrorResponse):
    pass
