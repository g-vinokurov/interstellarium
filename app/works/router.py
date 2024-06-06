# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Work, Contract, Project
from app.models import AssociationContractProject

from app.auth import get_current_user
from app.works import schema

router = APIRouter(tags=['works'])


@router.get('/api/works', response_model=list[schema.Work])
def api_works_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None,
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
    if name is not None and len(name) != 0:
        query = query.filter(Work.name.ilike(f'%{name}%'))
    if min_cost is not None:
        query = query.filter(Work.cost >= min_cost)
    if max_cost is not None:
        query = query.filter(Work.cost <= max_cost)

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


@router.post('/api/works', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_works_create(
    request: schema.CreateWorkRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        work = session.execute(
            select(Work).filter_by(name=request.name)
        ).scalar_one_or_none()

    if work is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    work = Work()
    work.name = request.name
    work.cost = request.cost

    with db.Session() as session:
        session.add(work)
        session.commit()

        work_id = work.id

    return JSONResponse({'id': work_id}, status.HTTP_201_CREATED)


@router.get('/api/works/{id}', response_model=list[schema.WorkProfile])
def api_works_get_one(id: int, current_user: User = Depends(get_current_user)):
    pass
