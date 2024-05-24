# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User

from app.auth import get_current_user
from app.users import schema

router = APIRouter(tags=['users'])


@router.post('/api/users', response_model=list[schema.User])
def get_all_users(filters: schema.UserFilters, current_user: User = Depends(get_current_user)):
    query = select(User.id, User.name, User.birthdate)
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(User.name.ilike(f'%{filters.name}%'))
    if filters.birthdate_to is not None:
        query = query.filter(User.birthdate <= filters.birthdate_to)
    if filters.birthdate_from is not None:
        query = query.filter(User.birthdate >= filters.birthdate_from)
    if filters.department_id is not None:
        query = query.filter(User.department_id == filters.department_id)

    with db.Session() as session:
        users = session.execute(query).all()

    data = []
    for user_id, user_name, user_birthdate in users:
        data.append({
            'id': user_id,
            'name': user_name,
            'birthdate': user_birthdate
        })

    return data


@router.post('/api/users/create', response_model=schema.CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: schema.CreateUserRequest, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        user = session.execute(
            select(User).filter_by(email=request.email)
        ).scalar_one_or_none()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User exists'
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

    return JSONResponse({'id': user_id}, status_code=status.HTTP_201_CREATED)
