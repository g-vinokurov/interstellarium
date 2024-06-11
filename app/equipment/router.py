# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Equipment, Department, Group

from app.auth import get_current_user
from app.equipment import schema

router = APIRouter(tags=['equipment'])


@router.get('/api/equipment', response_model=list[schema.Equipment])
def api_equipment_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Equipment.id,
        Equipment.name,
        Department.id,
        Department.name,
        Group.id,
        Group.name
    )
    query = query.join(
        Department,
        Department.id == Equipment.department_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Equipment.group_id,
        isouter=True
    )
    if name is not None and len(name) != 0:
        query = query.filter(Equipment.name.ilike(f'%{name}%'))

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
            },
            'group': {
                'id': row[4],
                'name': row[5],
            }
        }
        items.append(item)

    return items


@router.post('/api/equipment', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_equipment_create(
    request: schema.CreateEquipmentRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        equipment = session.execute(
            select(Equipment).filter_by(name=request.name)
        ).scalar_one_or_none()

    if equipment is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    equipment = Equipment()
    equipment.name = request.name

    with db.Session() as session:
        session.add(equipment)
        session.commit()

        equipment_id = equipment.id

    return JSONResponse({'id': equipment_id}, status.HTTP_201_CREATED)


@router.get('/api/equipment/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.EquipmentProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_equipment_get_one(
    id: int,
    current_user: User = Depends(get_current_user)
):
    pass
