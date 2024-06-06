# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Department

from app.auth import get_current_user
from app.departments import schema

router = APIRouter(tags=['departments'])


@router.get('/api/departments', response_model=list[schema.Department])
def api_departments_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Department.id,
        Department.name,
        User.id,
        User.name
    )
    query = query.join(
        User,
        User.id == Department.chief_id,
        isouter=True
    )
    if name is not None and len(name) != 0:
        query = query.filter(Department.name.ilike(f'%{name}%'))

    with db.Session() as session:
        data = session.execute(query).all()

    items = []
    for row in data:
        item = {
            'id': row[0],
            'name': row[1],
            'chief': {
                'id': row[2],
                'name': row[3],
            }
        }
        items.append(item)

    return items


@router.post('/api/departments', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_departments_create(
    request: schema.CreateDepartmentRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        department = session.execute(
            select(Department).filter_by(name=request.name)
        ).scalar_one_or_none()

    if department is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    department = Department()
    department.name = request.name

    with db.Session() as session:
        session.add(department)
        session.commit()

        department_id = department.id

    return JSONResponse({'id': department_id}, status.HTTP_201_CREATED)


@router.get('/api/departments/{id}', response_model=list[schema.DepartmentProfile])
def api_departments_get_one(id: int, current_user: User = Depends(get_current_user)):
    pass
