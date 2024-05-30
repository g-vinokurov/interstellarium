# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Contract

from app.auth import get_current_user
from app.contracts import schema

router = APIRouter(tags=['contracts'])


@router.post('/api/contracts', response_model=list[schema.Contract])
def get_contracts(
    filters: schema.ContractFilters,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Contract.id,
        Contract.name,
        Contract.start_date,
        Contract.finish_date
    )
    query = query.join(User, User.id == Contract.chief_id, isouter=True)
    query = query.join(Group, Group.id == Contract.group_id, isouter=True)
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(Contract.name.ilike(f'%{filters.name}%'))
    if filters.start_date is not None:
        query = query.filter(Contract.start_date >= filters.start_date)
    if filters.finish_date is not None:
        query = query.filter(Contract.finish_date <= filters.finish_date)

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


@router.post('/api/contracts/create', response_model=schema.CreateContractResponse, status_code=status.HTTP_201_CREATED)
def create_contract(
    request: schema.CreateContractRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        contract = session.execute(
            select(Contract).filter_by(name=request.name)
        ).scalar_one_or_none()

    if contract is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Contract exists'
        )

    if request.finish_date and request.start_date:
        if request.start_date > request.finish_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Start date cannot be greater than finish date'
            )

    contract = Contract()
    contract.name = request.name
    contract.start_date = request.start_date
    contract.finish_date = request.finish_date

    with db.Session() as session:
        session.add(contract)
        session.commit()

        contract_id = contract.id

    item = {'id': contract_id}
    return JSONResponse(item, status_code=status.HTTP_201_CREATED)
