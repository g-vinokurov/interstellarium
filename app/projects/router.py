# -*- coding: utf-8 -*-

from typing import Optional
from datetime import date, datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Project, Contract, Work
from app.models import AssociationContractProject
from app.models import AssignmentUserProject

from app.auth import get_current_user
from app.projects import schema

router = APIRouter(tags=['projects'])


@router.get('/api/projects', response_model=list[schema.Project])
def api_projects_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Project.id,
        Project.name,
        Project.start_date,
        Project.finish_date,
        User.id,
        User.name,
        Group.id,
        Group.name
    )
    query = query.join(
        User,
        User.id == Project.chief_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Project.group_id,
        isouter=True
    )
    if name is not None and len(name) != 0:
        query = query.filter(Project.name.ilike(f'%{name}%'))
    if start_date is not None:
        query = query.filter(Project.start_date >= start_date)
    if finish_date is not None:
        query = query.filter(Project.finish_date <= finish_date)

    with db.Session() as session:
        data = session.execute(query).all()

    items = []
    for row in data:
        item = {
            'id': row[0],
            'name': row[1],
            'start_date': row[2],
            'finish_date': row[3],
            'chief': {
                'id': row[4],
                'name': row[5]
            },
            'group': {
                'id': row[6],
                'name': row[7]
            }
        }
        items.append(item)

    return items


@router.post('/api/projects', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_projects_create(
    request: schema.CreateProjectRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        project = session.execute(
            select(Project).filter_by(name=request.name)
        ).scalar_one_or_none()

    if project is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    if request.finish_date and request.start_date:
        if request.start_date > request.finish_date:
            return JSONResponse(
                {'msg': 'invalid dates'}, status.HTTP_400_BAD_REQUEST
            )

    project = Project()
    project.name = request.name
    project.start_date = request.start_date
    project.finish_date = request.finish_date

    with db.Session() as session:
        session.add(project)
        session.commit()

        project_id = project.id

    return JSONResponse({'id': project_id}, status.HTTP_201_CREATED)


@router.get('/api/projects/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.ProjectProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_projects_get_one(
    id: int,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Project.id,
        Project.name,
        Project.start_date,
        Project.finish_date,
        User.id,
        User.name,
        Group.id,
        Group.name
    )
    query = query.join(
        User,
        User.id == Project.chief_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Project.group_id,
        isouter=True
    )
    query = query.where(Project.id == id)

    with db.Session() as session:
        project_data = session.execute(query).first()

    if project_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    project_id, project_name = project_data[0:2]
    project_start_date, project_finish_date = project_data[2:4]
    chief_id, chief_name, group_id, group_name = project_data[4:8]

    query = select(
        Contract.id,
        Contract.name
    )
    query = query.join(
        AssociationContractProject,
        AssociationContractProject.contract_id == Contract.id,
        isouter=False
    )
    query = query.join(
        Project,
        Project.id == AssociationContractProject.project_id,
        isouter=False
    )
    query = query.where(Project.id == project_id)

    with db.Session() as session:
        contracts_data = session.execute(query).all()

    query = select(
        Work.id,
        Work.name,
        Work.cost,
    )
    query = query.join(
        Project,
        Project.id == Work.project_id,
        isouter=True
    )
    query = query.join(
        Contract,
        Contract.id == Work.contract_id,
        isouter=True
    )
    query = query.where(Project.id == project_id)

    with db.Session() as session:
        works_data = session.execute(query).all()

    contracts = []
    for row in contracts_data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        contracts.append(item)

    works = []
    for row in works_data:
        item = {
            'id': row[0],
            'name': row[1],
            'cost': row[2]
        }
        works.append(item)

    if project_start_date is not None:
        project_start_date = str(project_start_date)
    if project_finish_date is not None:
        project_finish_date = str(project_finish_date)

    response = {
        'id': project_id,
        'name': project_name,
        'start_date': project_start_date,
        'finish_date': project_finish_date,
        'chief': {
            'id': chief_id,
            'name': chief_name
        },
        'group': {
            'id': group_id,
            'name': group_name
        },
        'contracts': contracts,
        'works': works
    }

    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/projects/{id}/chief', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_projects_update_chief(
    id: int,
    request: schema.UserID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    project = session.query(Project).get(id)
    chief = session.query(User).get(request.id)

    if project is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if project.chief_id is not None:
        unassignment = AssignmentUserProject()
        unassignment.project_id = project.id
        unassignment.user_id = project.chief_id
        unassignment.assignment_date = datetime.utcnow().date()
        unassignment.is_assigned = False

        session.add(unassignment)
        session.commit()

    if chief is None:
        project.chief_id = None
    else:
        project.chief_id = chief.id

    if project.chief_id is not None:
        assignment = AssignmentUserProject()
        assignment.project_id = project.id
        assignment.user_id = project.chief_id
        assignment.assignment_date = datetime.utcnow().date()
        assignment.is_assigned = True

        session.add(assignment)

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/projects/{id}/group', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_projects_update_group(
    id: int,
    request: schema.GroupID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    project = session.query(Project).get(id)
    group = session.query(Group).get(request.id)

    if project is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if group is None:
        project.group_id = None
    else:
        project.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/projects/{id}/contracts', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_projects_update_contracts(
    id: int,
    request: schema.ContractID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    project = session.query(Project).get(id)
    contract = session.query(Contract).get(request.id)

    if project is None or contract is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    association = session.query(AssociationContractProject).filter_by(
        contract_id=contract.id, project_id=project.id
    ).first()

    if association is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    association = AssociationContractProject()
    association.contract_id = contract.id
    association.project_id = project.id
    session.add(association)

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)
