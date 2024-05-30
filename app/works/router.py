# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Work, Contract, Project
from app.models import AssociationContractProject

from app.auth import get_current_user
from app.works import schema

router = APIRouter(tags=['works'])


@router.post('/api/works', response_model=list[schema.Work])
def get_works(
    filters: schema.WorkFilters,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Work.id,
        Work.name,
        Work.cost,
        Contract.id,
        Contract.name,
        Project.id,
        Project.name
    )
    query = query.join(
        AssociationContractProject,
        AssociationContractProject.id == Work.association_contract_project_id,
        isouter=True
    )
    query = query.join(
        Contract,
        Contract.id == AssociationContractProject.contract_id,
        isouter=True
    )
    query = query.join(
        Project,
        Project.id == AssociationContractProject.project_id,
        isouter=True
    )
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(Work.name.ilike(f'%{filters.name}%'))
    if filters.min_cost is not None:
        query = query.filter(Work.cost >= filters.min_cost)
    if filters.max_cost is not None:
        query = query.filter(Work.cost <= filters.max_cost)

    with db.Session() as session:
        data = session.execute(query).all()

    items = []
    for row in data:
        item = {
            'id': row[0],
            'name': row[1],
            'cost': row[2],
            'contract': {
                'id': row[3],
                'name': row[4],
            },
            'project': {
                'id': row[5],
                'name': row[6],
            }
        }
        items.append(item)

    return items


@router.post('/api/works/create', response_model=schema.CreateWorkResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(
    request: schema.CreateWorkRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        work = session.execute(
            select(Work).filter_by(name=request.name)
        ).scalar_one_or_none()

    if work is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Equipment exists'
        )

    work = Work()
    work.name = request.name
    work.cost = request.cost

    with db.Session() as session:
        session.add(work)
        session.commit()

        work_id = work.id

    item = {'id': work_id}
    return JSONResponse(item, status_code=status.HTTP_201_CREATED)
