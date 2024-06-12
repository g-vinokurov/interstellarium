# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Work, Contract, Project, Group

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
        Contract,
        Contract.id == Work.contract_id,
        isouter=True
    )
    query = query.join(
        Project,
        Project.id == Work.project_id,
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


@router.get('/api/works/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.WorkProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_works_get_one(
    id: int,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Work.id,
        Work.name,
        Work.cost,
        Contract.id,
        Contract.name,
        Project.id,
        Project.name,
        Group.id,
        Group.name
    )
    query = query.join(
        Contract,
        Contract.id == Work.contract_id,
        isouter=True
    )
    query = query.join(
        Project,
        Project.id == Work.project_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Work.group_id,
        isouter=True
    )
    query = query.where(Work.id == id)

    with db.Session() as session:
        work_data = session.execute(query).first()

    if work_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    work_id, work_name, work_cost = work_data[0:3]
    contract_id, contract_name = work_data[3:5]
    project_id, project_name = work_data[5:7]
    group_id, group_name = work_data[7:9]

    response = {
        'id': work_id,
        'name': work_name,
        'cost': work_cost,
        'contract': {
            'id': contract_id,
            'name': contract_name
        },
        'project': {
            'id': project_id,
            'name': project_name
        },
        'group': {
            'id': group_id,
            'name': group_name
        },
    }
    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/works/{id}/contract', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_works_update_contract(
    id: int,
    request: schema.ContractID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    work = session.query(Work).get(id)
    contract = session.query(Contract).get(request.id)

    if work is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    # TODO: проверить доступ work.group к work.contract

    if contract is None:
        work.contract_id = None
    else:
        work.contract_id = contract.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/works/{id}/project', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_works_update_project(
    id: int,
    request: schema.ProjectID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    work = session.query(Work).get(id)
    project = session.query(Project).get(request.id)

    if work is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    # TODO: проверить доступ work.group к work.project

    if project is None:
        work.project_id = None
    else:
        work.project_id = project.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/works/{id}/group', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_works_update_group(
    id: int,
    request: schema.GroupID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    work = session.query(Work).get(id)
    group = session.query(Group).get(request.id)

    if work is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    # TODO: проверить доступ work.group к work.contract и work.project

    if group is None:
        work.group_id = None
    else:
        work.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)
