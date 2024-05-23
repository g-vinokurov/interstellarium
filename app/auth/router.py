# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, status

from app.db import db
from app.models import User

from app.auth.jwt import create_access_token
from app.auth import schema

router = APIRouter(tags=['auth'])


@router.post('/api/auth/login', response_model=schema.Token)
def login(request: schema.LoginRequest):
    session = db.get()
    user = session.query(User).filter(User.email == request.email).first()

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
