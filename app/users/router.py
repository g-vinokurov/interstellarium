# -*- coding: utf-8 -*-

from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Department

from app.auth import get_current_user
from app.users import schema

router = APIRouter(tags=['users'])


@router.get('/api/users', response_model=list[schema.User])
def api_users_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    birthdate_from: Optional[date] = None,
    birthdate_to: Optional[date] = None,
    department_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        User.id,
        User.name,
        Department.id,
        Department.name
    )
    query = query.join(
        Department,
        Department.id == User.department_id,
        isouter=True
    )
    if id is not None:
        query = query.filter(User.id == id)
    if name is not None and len(name) != 0:
        query = query.filter(User.name.ilike(f'%{name}%'))
    if birthdate_to is not None:
        query = query.filter(User.birthdate <= birthdate_to)
    if birthdate_from is not None:
        query = query.filter(User.birthdate >= birthdate_from)
    if department_id is not None:
        query = query.filter(User.department_id == department_id)

    with db.Session() as session:
        data = session.execute(query).all()

    items = []
    for row in data:
        item = {
            'id': row[0],
            'name': row[1],
            'department': {
                'id': row[2],
                'name': row[3],
            }
        }
        items.append(item)

    return JSONResponse(items, status.HTTP_200_OK)


@router.post('/api/users', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_users_create(
    request: schema.CreateUserRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        user = session.execute(
            select(User).filter_by(email=request.email)
        ).scalar_one_or_none()

    if user is not None:
        return JSONResponse(
            {'msg': 'user exists'}, status.HTTP_400_BAD_REQUEST
        )

    user = User()
    user.email = request.email
    user.set_password(request.password)
    user.is_superuser = False
    user.is_admin = request.is_admin
    user.name = request.name
    user.birthdate = request.birthdate

    with db.Session() as session:
        session.add(user)
        session.commit()

        user_id = user.id

    return JSONResponse({'id': user_id}, status.HTTP_201_CREATED)


@router.get('/api/users/{id}', response_model=list[schema.UserProfile])
def api_users_get_one(id: int, current_user: User = Depends(get_current_user)):
    pass
