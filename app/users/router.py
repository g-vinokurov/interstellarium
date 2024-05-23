# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status

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
        query = query.filter(User.name.ilike(filters.name))
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
