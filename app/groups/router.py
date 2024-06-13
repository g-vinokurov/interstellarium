# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Work, Contract, Project, Equipment
from app.models import AssociationUserGroup

from app.auth import get_current_user
from app.groups import schema

router = APIRouter(tags=['groups'])


@router.get('/api/groups', response_model=list[schema.Group])
def api_groups_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Group.id,
        Group.name,
    )
    if name is not None and len(name) != 0:
        query = query.filter(Group.name.ilike(f'%{name}%'))

    with db.Session() as session:
        data = session.execute(query).all()

    items = []
    for row in data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        items.append(item)

    return items


@router.post('/api/groups', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_groups_create(
    request: schema.CreateGroupRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        group = session.execute(
            select(Group).filter_by(name=request.name)
        ).scalar_one_or_none()

    if group is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    group = Group()
    group.name = request.name

    with db.Session() as session:
        session.add(group)
        session.commit()

        group_id = group.id

    return JSONResponse({'id': group_id}, status.HTTP_201_CREATED)


@router.get('/api/groups/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.GroupProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_groups_get_one(
    id: int,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Group.id,
        Group.name,
    )
    query = query.where(Group.id == id)

    with db.Session() as session:
        group_data = session.execute(query).first()

    if group_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    group_id, group_name = group_data[0:2]

    query = select(
        User.id,
        User.name
    )
    query = query.join(
        AssociationUserGroup,
        AssociationUserGroup.user_id == User.id,
        isouter=True
    )
    query = query.where(AssociationUserGroup.group_id == group_id)

    with db.Session() as session:
        users_data = session.execute(query).all()

    query = select(
        Work.id,
        Work.name,
        Work.cost,
    )
    query = query.where(Work.group_id == group_id)

    with db.Session() as session:
        works_data = session.execute(query).all()

    query = select(
        Contract.id,
        Contract.name,
    )
    query = query.where(Contract.group_id == group_id)

    with db.Session() as session:
        contracts_data = session.execute(query).all()

    query = select(
        Project.id,
        Project.name,
    )
    query = query.where(Project.group_id == group_id)

    with db.Session() as session:
        projects_data = session.execute(query).all()

    query = select(
        Equipment.id,
        Equipment.name,
    )
    query = query.where(Equipment.group_id == group_id)

    with db.Session() as session:
        equipment_data = session.execute(query).all()

    users = []
    for row in users_data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        users.append(item)

    works = []
    for row in works_data:
        item = {
            'id': row[0],
            'name': row[1],
            'cost': row[2]
        }
        works.append(item)

    contracts = []
    for row in contracts_data:
        item = {
            'id': row[0],
            'name': row[1],
        }
        contracts.append(item)

    projects = []
    for row in projects_data:
        item = {
            'id': row[0],
            'name': row[1],
        }
        projects.append(item)

    equipment = []
    for row in equipment_data:
        item = {
            'id': row[0],
            'name': row[1],
        }
        equipment.append(item)

    response = {
        'id': group_id,
        'name': group_name,
        'users': users,
        'works': works,
        'contracts': contracts,
        'projects': projects,
        'equipment': equipment
    }
    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/groups/{id}/users', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_groups_update_users(
    id: int,
    request: schema.UserID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    group = session.query(Group).get(id)
    user = session.query(User).get(request.id)

    if group is None or user is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    association = session.query(AssociationUserGroup).filter_by(
        group_id=group.id, user_id=user.id
    ).first()

    if association is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    association = AssociationUserGroup()
    association.group_id = group.id
    association.user_id = user.id
    session.add(association)

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/groups/{id}/works', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_groups_update_works(
    id: int,
    request: schema.WorkID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    group = session.query(Group).get(id)
    work = session.query(Work).get(request.id)

    if group is None or work is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    work.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/groups/{id}/contracts', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_groups_update_contracts(
    id: int,
    request: schema.ContractID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    group = session.query(Group).get(id)
    contract = session.query(Contract).get(request.id)

    if group is None or contract is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    contract.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/groups/{id}/projects', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_groups_update_projects(
    id: int,
    request: schema.ProjectID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    group = session.query(Group).get(id)
    project = session.query(Project).get(request.id)

    if group is None or project is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    project.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/groups/{id}/equipment', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_groups_update_equipment(
    id: int,
    request: schema.EquipmentID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    group = session.query(Group).get(id)
    equipment = session.query(Equipment).get(request.id)

    if group is None or equipment is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    equipment.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)
