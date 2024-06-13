# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Department, Equipment
from app.models import AssignmentEquipmentDepartment

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


@router.get('/api/departments/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.DepartmentProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_departments_get_one(
    id: int,
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
    query = query.where(Department.id == id)

    with db.Session() as session:
        department_data = session.execute(query).first()

    if department_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    department_id, department_name, chief_id, chief_name = department_data

    query = select(
        User.id,
        User.name
    ).where(
        User.department_id == department_id
    )

    with db.Session() as session:
        users_data = session.execute(query).all()

    query = select(
        Equipment.id,
        Equipment.name
    ).where(
        Equipment.department_id == department_id
    )

    with db.Session() as session:
        equipment_data = session.execute(query).all()

    users = []
    for row in users_data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        users.append(item)

    equipment = []
    for row in equipment_data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        equipment.append(item)

    response = {
        'id': department_id,
        'name': department_name,
        'chief': {
            'id': chief_id,
            'name': chief_name
        },
        'users': users,
        'equipment': equipment
    }

    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/departments/{id}/chief', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_departments_update_chief(
    id: int,
    request: schema.UserID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    department = session.query(Department).get(id)
    chief = session.query(User).get(request.id)

    if department is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if chief is None:
        department.chief_id = None
    else:
        department.chief_id = chief.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/departments/{id}/equipment', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_departments_update_equipment(
    id: int,
    request: schema.EquipmentID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    department = session.query(Department).get(id)
    equipment = session.query(Equipment).get(request.id)

    if department is None or equipment is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if equipment.department_id is not None:
        unassignment = AssignmentEquipmentDepartment()
        unassignment.equipment_id = equipment.id
        unassignment.department_id = equipment.department_id
        unassignment.assignment_date = datetime.utcnow().date()
        unassignment.is_assigned = False

        session.add(unassignment)
        session.commit()

    equipment.department_id = department.id

    assignment = AssignmentEquipmentDepartment()
    assignment.equipment_id = equipment.id
    assignment.department_id = equipment.department_id
    assignment.assignment_date = datetime.utcnow().date()
    assignment.is_assigned = True

    session.add(assignment)
    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/departments/{id}/users', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_departments_update_users(
    id: int,
    request: schema.UserID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    department = session.query(Department).get(id)
    user = session.query(User).get(request.id)

    if department is None or user is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    user.department_id = department.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)
