# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group

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
            {'msg': 'group exists'}, status.HTTP_400_BAD_REQUEST
        )

    group = Group()
    group.name = request.name

    with db.Session() as session:
        session.add(group)
        session.commit()

        group_id = group.id

    return JSONResponse({'id': group_id}, status.HTTP_201_CREATED)


@router.get('/api/groups/{id}', response_model=list[schema.GroupProfile])
def api_groups_get_one(id: int, current_user: User = Depends(get_current_user)):
    pass
