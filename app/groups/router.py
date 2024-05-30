# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group

from app.auth import get_current_user
from app.groups import schema

router = APIRouter(tags=['groups'])


@router.post('/api/groups', response_model=list[schema.Group])
def get_groups(
    filters: schema.GroupFilters,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Group.id,
        Group.name,
    )
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(Group.name.ilike(f'%{filters.name}%'))

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


@router.post('/api/groups/create', response_model=schema.CreateGroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    request: schema.CreateGroupRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        group = session.execute(
            select(Group).filter_by(name=request.name)
        ).scalar_one_or_none()

    if group is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Group exists'
        )

    group = Group()
    group.name = request.name

    with db.Session() as session:
        session.add(group)
        session.commit()

        group_id = group.id

    item = {'id': group_id}
    return JSONResponse(item, status_code=status.HTTP_201_CREATED)
