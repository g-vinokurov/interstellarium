# -*- coding: utf-8 -*-

from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Contract

from app.auth import get_current_user
from app.contracts import schema

router = APIRouter(tags=['contracts'])


@router.get('/api/contracts', response_model=list[schema.Contract])
def api_contracts_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Contract.id,
        Contract.name,
        Contract.start_date,
        Contract.finish_date,
        User.id,
        User.name,
        Group.id,
        Group.name
    )
    query = query.join(
        User,
        User.id == Contract.chief_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Contract.group_id,
        isouter=True
    )
    if name is not None and len(name) != 0:
        query = query.filter(Contract.name.ilike(f'%{name}%'))
    if start_date is not None:
        query = query.filter(Contract.start_date >= start_date)
    if finish_date is not None:
        query = query.filter(Contract.finish_date <= finish_date)

    with db.Session() as session:
        data = session.execute(query).all()

    items = []
    for row in data:
        item = {
            'id': row[0],
            'name': row[1],
            'start_date': row[2],
            'finish_date': row[3],
            'chief': {
                'id': row[4],
                'name': row[5]
            },
            'group': {
                'id': row[6],
                'name': row[7]
            }
        }
        items.append(item)

    return items


@router.post('/api/contracts', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_contracts_create(
    request: schema.CreateContractRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        contract = session.execute(
            select(Contract).filter_by(name=request.name)
        ).scalar_one_or_none()

    if contract is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    if request.finish_date and request.start_date:
        if request.start_date > request.finish_date:
            return JSONResponse(
                {'msg': 'invalid dates'}, status.HTTP_400_BAD_REQUEST
            )

    contract = Contract()
    contract.name = request.name
    contract.start_date = request.start_date
    contract.finish_date = request.finish_date

    with db.Session() as session:
        session.add(contract)
        session.commit()

        contract_id = contract.id

    return JSONResponse({'id': contract_id}, status.HTTP_201_CREATED)


@router.get('/api/contracts/{id}', response_model=list[schema.ContractProfile])
def api_contracts_get_one(id: int, current_user: User = Depends(get_current_user)):
    pass
