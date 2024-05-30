# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Equipment, Department, Group

from app.auth import get_current_user
from app.equipment import schema

router = APIRouter(tags=['equipment'])


@router.post('/api/equipment', response_model=list[schema.Equipment])
def get_equipment(
    filters: schema.EquipmentFilters,
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
    query = query.join(Department, Department.id == Equipment.department_id, isouter=True)
    query = query.join(Group, Group.id == Equipment.group_id, isouter=True)
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(Equipment.name.ilike(f'%{filters.name}%'))

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


@router.post('/api/equipment/create', response_model=schema.CreateEquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(
    request: schema.CreateEquipmentRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        equipment = session.execute(
            select(Equipment).filter_by(name=request.name)
        ).scalar_one_or_none()

    if equipment is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Equipment exists'
        )

    equipment = Equipment()
    equipment.name = request.name

    with db.Session() as session:
        session.add(equipment)
        session.commit()

        equipment_id = equipment.id

    item = {'id': equipment_id}
    return JSONResponse(item, status_code=status.HTTP_201_CREATED)
