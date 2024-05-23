# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, status

from sqlalchemy import select

from app.db import db
from app.models import User

from app.auth.jwt import create_access_token
from app.auth import schema

router = APIRouter(tags=['auth'])


@router.post('/api/auth/login', response_model=schema.Token)
def login(request: schema.LoginRequest):
    with db.Session() as session:
        user = session.execute(
            select(User).filter_by(email=request.email)
        ).scalar_one()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid Credentials'
        )

    if not user.check_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Password'
        )

    # Generate a JWT Token
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
