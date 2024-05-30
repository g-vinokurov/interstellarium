# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


class Contract(BaseModel):
    id: int


class ContractFilters(BaseModel):
    name: Optional[str] = None


class CreateContractRequest(BaseModel):
    name: str


class CreateContractResponse(BaseModel):
    id: int
