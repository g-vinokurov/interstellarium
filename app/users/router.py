# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select

from app.db import db
from app.models import User

from app.auth import get_current_user
from app.users import schema

router = APIRouter(tags=['users'])


@router.get('/api/users', response_model=list[schema.User])
def get_all_users(current_user: User = Depends(get_current_user)):
    with db.Session() as session:
        users = session.execute(
            select(User)
        ).scalars()

    return [{'email': user.email} for user in users]
