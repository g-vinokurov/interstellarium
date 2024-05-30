# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Department

from app.auth import get_current_user
from app.departments import schema

router = APIRouter(tags=['departments'])


@router.post('/api/departments', response_model=list[schema.Department])
def get_departments(
    filters: schema.DepartmentFilters,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Department.id,
        Department.name,
        User.id,
        User.name
    )
    query = query.join(User, User.id == Department.chief_id, isouter=True)
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(Department.name.ilike(f'%{filters.name}%'))

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


@router.post('/api/departments/create', response_model=schema.CreateDepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    request: schema.CreateDepartmentRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        department = session.execute(
            select(Department).filter_by(name=request.name)
        ).scalar_one_or_none()

    if department is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Department exists'
        )

    department = Department()
    department.name = request.name

    with db.Session() as session:
        session.add(department)
        session.commit()

        department_id = department.id

    item = {'id': department_id}
    return JSONResponse(item, status_code=status.HTTP_201_CREATED)
