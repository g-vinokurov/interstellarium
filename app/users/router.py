# -*- coding: utf-8 -*-

from typing import Optional
from datetime import date, datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Department, Group, Contract, Project
from app.models import AssociationUserGroup
from app.models import AssignmentUserProject
from app.models import AssignmentUserContract

from app.auth import get_current_user
from app.users import schema

router = APIRouter(tags=['users'])


@router.get('/api/users', response_model=list[schema.User])
def api_users_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    birthdate_from: Optional[date] = None,
    birthdate_to: Optional[date] = None,
    department_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        User.id,
        User.name,
        Department.id,
        Department.name
    )
    query = query.join(
        Department,
        Department.id == User.department_id,
        isouter=True
    )
    if id is not None:
        query = query.filter(User.id == id)
    if name is not None and len(name) != 0:
        query = query.filter(User.name.ilike(f'%{name}%'))
    if birthdate_to is not None:
        query = query.filter(User.birthdate <= birthdate_to)
    if birthdate_from is not None:
        query = query.filter(User.birthdate >= birthdate_from)
    if department_id is not None:
        query = query.filter(User.department_id == department_id)

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
            }
        }
        items.append(item)

    return JSONResponse(items, status.HTTP_200_OK)


@router.post('/api/users', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_users_create(
    request: schema.CreateUserRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        user = session.execute(
            select(User).filter_by(email=request.email)
        ).scalar_one_or_none()

    if user is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    user = User()
    user.email = request.email
    user.set_password(request.password)
    user.is_superuser = False
    user.is_admin = request.is_admin
    user.name = request.name
    user.birthdate = request.birthdate

    with db.Session() as session:
        session.add(user)
        session.commit()

        user_id = user.id

    return JSONResponse({'id': user_id}, status.HTTP_201_CREATED)


@router.get('/api/users/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.UserProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_users_get_one(
    id: int,
    current_user: User = Depends(get_current_user)
):
    query = select(
        User.id,
        User.name,
        User.birthdate,
        User.is_admin,
        Department.id,
        Department.name
    )
    query = query.join(
        Department,
        Department.id == User.department_id,
        isouter=True
    )
    query = query.where(User.id == id)

    with db.Session() as session:
        user_data = session.execute(query).first()

    if user_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    user_id, user_name, user_birthdate, user_is_admin = user_data[0:4]
    department_id, department_name = user_data[4:6]

    query = select(
        Group.id,
        Group.name
    )
    query = query.join(
        AssociationUserGroup,
        AssociationUserGroup.group_id == Group.id,
        isouter=True
    )
    query = query.where(AssociationUserGroup.user_id == user_id)

    with db.Session() as session:
        groups_data = session.execute(query).all()

    query = select(
        AssignmentUserProject.id,
        AssignmentUserProject.assignment_date,
        AssignmentUserProject.is_assigned,
        Project.id,
        Project.name
    )
    query = query.join(
        Project,
        Project.id == AssignmentUserProject.project_id,
        isouter=True
    )
    query = query.where(AssignmentUserProject.user_id == user_id)

    with db.Session() as session:
        projects_assignments_data = session.execute(query).all()

    query = select(
        AssignmentUserContract.id,
        AssignmentUserContract.assignment_date,
        AssignmentUserContract.is_assigned,
        Contract.id,
        Contract.name
    )
    query = query.join(
        Contract,
        Contract.id == AssignmentUserContract.contract_id,
        isouter=True
    )
    query = query.where(AssignmentUserContract.user_id == user_id)

    with db.Session() as session:
        contracts_assignments_data = session.execute(query).all()

    groups = []
    for row in groups_data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        groups.append(item)

    projects_assignments = []
    for row in projects_assignments_data:
        assignment_date = row[1]
        if assignment_date is not None:
            assignment_date = str(assignment_date)

        item = {
            'id': row[0],
            'assignment_date': assignment_date,
            'is_assigned': row[2],
            'project': {
                'id': row[3],
                'name': row[4]
            }
        }
        projects_assignments.append(item)

    contracts_assignments = []
    for row in contracts_assignments_data:
        assignment_date = row[1]
        if assignment_date is not None:
            assignment_date = str(assignment_date)

        item = {
            'id': row[0],
            'assignment_date': assignment_date,
            'is_assigned': row[2],
            'contract': {
                'id': row[3],
                'name': row[4]
            }
        }
        contracts_assignments.append(item)

    if user_birthdate is not None:
        user_birthdate = str(user_birthdate)

    contracts_assignments.sort(key=lambda x: x['id'], reverse=True)
    projects_assignments.sort(key=lambda x: x['id'], reverse=True)

    response = {
        'id': user_id,
        'name': user_name,
        'birthdate': user_birthdate,
        'is_admin': user_is_admin,
        'department': {
            'id': department_id,
            'name': department_name
        },
        'groups': groups,
        'projects_assignments': projects_assignments,
        'contracts_assignments': contracts_assignments
    }
    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/users/{id}/department', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_users_update_department(
    id: int,
    request: schema.DepartmentID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    user = session.query(User).get(id)
    department = session.query(Department).get(request.id)

    if user is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if department is None:
        user.department_id = None
    else:
        user.department_id = department.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/users/{id}/groups', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_users_update_department(
    id: int,
    request: schema.GroupID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    user = session.query(User).get(id)
    group = session.query(Group).get(request.id)

    if user is None or group is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    association = session.query(AssociationUserGroup).filter_by(
        user_id=user.id, group_id=group.id
    ).first()

    if association is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    association = AssociationUserGroup()
    association.user_id = user.id
    association.group_id = group.id
    session.add(association)
    session.commit()

    projects = session.query(Project).filter(
        Project.group_id == group.id
    ).all()
    contracts = session.query(Contract).filter(
        Contract.group_id == group.id
    ).all()

    assignments = []
    for contract in contracts:
        assignment = AssignmentUserContract()
        assignment.user_id = user.id
        assignment.contract_id = contract.id
        assignment.assignment_date = datetime.utcnow().date()
        assignment.is_assigned = True
        assignments.append(assignment)

    session.add_all(assignments)
    session.commit()

    assignments = []
    for project in projects:
        assignment = AssignmentUserProject()
        assignment.user_id = user.id
        assignment.project_id = project.id
        assignment.assignment_date = datetime.utcnow().date()
        assignment.is_assigned = True
        assignments.append(assignment)

    session.add_all(assignments)
    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)
