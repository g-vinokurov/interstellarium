# -*- coding: utf-8 -*-

from typing import Optional
from datetime import date, datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Contract, Project, Work
from app.models import AssociationContractProject
from app.models import AssignmentUserContract
from app.models import AssociationUserGroup

from app.auth import get_current_user
from app.contracts import schema

router = APIRouter(tags=['contracts'])


@router.get('/api/contracts', response_model=list[schema.Contract])
def api_contracts_get_all(
    id: Optional[int] = None,
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Contract.id,
        Contract.name,
        Contract.start_date,
        Contract.finish_date,
        User.id,
        User.name,
        Group.id,
        Group.name
    )
    query = query.join(
        User,
        User.id == Contract.chief_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Contract.group_id,
        isouter=True
    )
    if name is not None and len(name) != 0:
        query = query.filter(Contract.name.ilike(f'%{name}%'))
    if start_date is not None:
        query = query.filter(Contract.start_date >= start_date)
    if finish_date is not None:
        query = query.filter(Contract.finish_date <= finish_date)

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


@router.post('/api/contracts', status_code=status.HTTP_201_CREATED, responses={
    201: {'model': schema.CreatedResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
})
def api_contracts_create(
    request: schema.CreateContractRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    with db.Session() as session:
        contract = session.execute(
            select(Contract).filter_by(name=request.name)
        ).scalar_one_or_none()

    if contract is not None:
        return JSONResponse(
            {'msg': 'item exists'}, status.HTTP_400_BAD_REQUEST
        )

    if request.finish_date and request.start_date:
        if request.start_date > request.finish_date:
            return JSONResponse(
                {'msg': 'invalid dates'}, status.HTTP_400_BAD_REQUEST
            )

    contract = Contract()
    contract.name = request.name
    contract.start_date = request.start_date
    contract.finish_date = request.finish_date

    with db.Session() as session:
        session.add(contract)
        session.commit()

        contract_id = contract.id

    return JSONResponse({'id': contract_id}, status.HTTP_201_CREATED)


@router.get('/api/contracts/{id}', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.ContractProfile},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_contracts_get_one(
    id: int,
    current_user: User = Depends(get_current_user)
):
    query = select(
        Contract.id,
        Contract.name,
        Contract.start_date,
        Contract.finish_date,
        User.id,
        User.name,
        Group.id,
        Group.name
    )
    query = query.join(
        User,
        User.id == Contract.chief_id,
        isouter=True
    )
    query = query.join(
        Group,
        Group.id == Contract.group_id,
        isouter=True
    )
    query = query.where(Contract.id == id)

    with db.Session() as session:
        contract_data = session.execute(query).first()

    if contract_data is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    contract_id, contract_name = contract_data[0:2]
    contract_start_date, contract_finish_date = contract_data[2:4]
    chief_id, chief_name, group_id, group_name = contract_data[4:8]

    query = select(
        Project.id,
        Project.name
    )
    query = query.join(
        AssociationContractProject,
        AssociationContractProject.project_id == Project.id,
        isouter=False
    )
    query = query.join(
        Contract,
        Contract.id == AssociationContractProject.contract_id,
        isouter=False
    )
    query = query.where(Contract.id == contract_id)

    with db.Session() as session:
        projects_data = session.execute(query).all()

    query = select(
        Work.id,
        Work.name,
        Work.cost,
    )
    query = query.join(
        Contract,
        Contract.id == Work.contract_id,
        isouter=True
    )
    query = query.join(
        Project,
        Project.id == Work.project_id,
        isouter=True
    )
    query = query.where(Contract.id == contract_id)

    with db.Session() as session:
        works_data = session.execute(query).all()

    query = select(
        User.id
    )
    query = query.join(
        AssociationUserGroup,
        AssociationUserGroup.user_id == User.id,
        isouter=False
    )
    query = query.join(
        Group,
        Group.id == AssociationUserGroup.group_id,
        isouter=False
    )
    query = query.join(
        Project,
        Project.group_id == Group.id,
        isouter=False
    )
    query = query.join(
        AssociationContractProject,
        AssociationContractProject.project_id == Project.id,
        isouter=False
    )
    query = query.join(
        Contract,
        Contract.id == AssociationContractProject.contract_id,
        isouter=False
    )
    query = query.where(Contract.id == contract_id)

    with db.Session() as session:
        users_data = session.execute(query).all()

    projects = []
    for row in projects_data:
        item = {
            'id': row[0],
            'name': row[1]
        }
        projects.append(item)

    works = []
    for row in works_data:
        item = {
            'id': row[0],
            'name': row[1],
            'cost': row[2]
        }
        works.append(item)

    if contract_start_date is not None:
        contract_start_date = str(contract_start_date)
    if contract_finish_date is not None:
        contract_finish_date = str(contract_finish_date)

    users_number = max(len(users_data), 1)
    works_total_cost = sum(x['cost'] for x in works)
    effectivity = works_total_cost / users_number

    response = {
        'id': contract_id,
        'name': contract_name,
        'start_date': contract_start_date,
        'finish_date': contract_finish_date,
        'effectivity': effectivity,
        'works_total_cost': works_total_cost,
        'users_number': users_number,
        'chief': {
            'id': chief_id,
            'name': chief_name
        },
        'group': {
            'id': group_id,
            'name': group_name
        },
        'projects': projects,
        'works': works
    }

    return JSONResponse(response, status.HTTP_200_OK)


@router.put('/api/contracts/{id}/chief', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_contracts_update_chief(
    id: int,
    request: schema.UserID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    contract = session.query(Contract).get(id)
    chief = session.query(User).get(request.id)

    if contract is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if contract.chief_id is not None:
        unassignment = AssignmentUserContract()
        unassignment.contract_id = contract.id
        unassignment.user_id = contract.chief_id
        unassignment.assignment_date = datetime.utcnow().date()
        unassignment.is_assigned = False

        session.add(unassignment)
        session.commit()

    if chief is None:
        contract.chief_id = None
    else:
        contract.chief_id = chief.id

    if contract.chief_id is not None:
        assignment = AssignmentUserContract()
        assignment.contract_id = contract.id
        assignment.user_id = contract.chief_id
        assignment.assignment_date = datetime.utcnow().date()
        assignment.is_assigned = True

        session.add(assignment)

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/contracts/{id}/group', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_contracts_update_group(
    id: int,
    request: schema.GroupID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    contract = session.query(Contract).get(id)
    group = session.query(Group).get(request.id)

    if contract is None:
        return JSONResponse(
            {'msg': 'item not found'}, status.HTTP_404_NOT_FOUND
        )

    if group is None:
        contract.group_id = None
    else:
        contract.group_id = group.id

    session.commit()
    return JSONResponse({'msg': 'ok'}, status.HTTP_200_OK)


@router.put('/api/contracts/{id}/projects', status_code=status.HTTP_200_OK, responses={
    200: {'model': schema.OkResponse},
    400: {'model': schema.BadRequestError},
    401: {'model': schema.UnauthorizedError},
    403: {'model': schema.ForbiddenError},
    404: {'model': schema.NotFoundError}
})
def api_contracts_update_projects(
    id: int,
    request: schema.ProjectID,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        return JSONResponse(
            {'msg': 'access denied'}, status.HTTP_403_FORBIDDEN
        )

    session = db.Session()

    contract = session.query(Contract).get(id)
    project = session.query(Project).get(request.id)

    if contract is None or project is None:
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
