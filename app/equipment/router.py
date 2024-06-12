# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Equipment, Department, Group
from app.models import AssignmentEquipmentDepartment
from app.models import AssignmentEquipmentGroup

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
    query = query.where(Equipment.id == id)

    with db.Session() as session:
        equipment_data = session.execute(query).first()

    if equipment_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    equipment_id, equipment_name = equipment_data[0:2]
    department_id, department_name = equipment_data[2:4]
    group_id, group_name = equipment_data[4:6]

    query = select(
        AssignmentEquipmentDepartment.id,
        AssignmentEquipmentDepartment.assignment_date,
        AssignmentEquipmentDepartment.is_assigned,
        Department.id,
        Department.name
    )
    query = query.join(
        Department,
        Department.id == AssignmentEquipmentDepartment.department_id,
        isouter=True
    )
    query = query.where(
        AssignmentEquipmentDepartment.equipment_id == equipment_id
    )

    with db.Session() as session:
        departments_assignments_data = session.execute(query).all()

    query = select(
        AssignmentEquipmentGroup.id,
        AssignmentEquipmentGroup.assignment_date,
        AssignmentEquipmentGroup.is_assigned,
        Group.id,
        Group.name
    )
    query = query.join(
        Group,
        Group.id == AssignmentEquipmentGroup.group_id,
        isouter=True
    )
    query = query.where(
        AssignmentEquipmentGroup.equipment_id == equipment_id
    )

    with db.Session() as session:
        groups_assignments_data = session.execute(query).all()

    departments_assignments = []
    for row in departments_assignments_data:
        assignment_date = row[1]
        if assignment_date is not None:
            assignment_date = str(assignment_date)

        item = {
            'id': row[0],
            'assignment_date': assignment_date,
            'is_assigned': row[2],
            'department': {
                'id': row[3],
                'name': row[4]
            }
        }
        departments_assignments.append(item)

    groups_assignments = []
    for row in groups_assignments_data:
        assignment_date = row[1]
        if assignment_date is not None:
            assignment_date = str(assignment_date)

        item = {
            'id': row[0],
            'assignment_date': assignment_date,
            'is_assigned': row[2],
            'group': {
                'id': row[3],
                'name': row[4]
            }
        }
        groups_assignments.append(item)

    response = {
        'id': equipment_id,
        'name': equipment_name,
        'department': {
            'id': department_id,
            'name': department_name
        },
        'group': {
            'id': group_id,
            'name': group_name
        },
        'departments_assignments': departments_assignments,
        'groups_assignments': groups_assignments
    }
    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/equipment/{id}/department', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_equipment_update_department(
    id: int,
    request: schema.DepartmentID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    equipment = session.query(Equipment).get(id)
    department = session.query(Department).get(request.id)

    if equipment is None:
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

    if department is None:
        equipment.department_id = None
    else:
        equipment.department_id = department.id

    if equipment.department_id is not None:
        assignment = AssignmentEquipmentDepartment()
        assignment.equipment_id = equipment.id
        assignment.department_id = equipment.department_id
        assignment.assignment_date = datetime.utcnow().date()
        assignment.is_assigned = True

        session.add(assignment)

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/equipment/{id}/group', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_equipment_update_group(
    id: int,
    request: schema.GroupID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    equipment = session.query(Equipment).get(id)
    group = session.query(Group).get(request.id)

    if equipment is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if equipment.group_id is not None:
        unassignment = AssignmentEquipmentGroup()
        unassignment.equipment_id = equipment.id
        unassignment.group_id = equipment.group_id
        unassignment.assignment_date = datetime.utcnow().date()
        unassignment.is_assigned = False

        session.add(unassignment)
        session.commit()

    if group is None:
        equipment.group_id = None
    else:
        equipment.group_id = group.id

    if equipment.group_id is not None:
        assignment = AssignmentEquipmentGroup()
        assignment.equipment_id = equipment.id
        assignment.group_id = equipment.group_id
        assignment.assignment_date = datetime.utcnow().date()
        assignment.is_assigned = True

        session.add(assignment)

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)
