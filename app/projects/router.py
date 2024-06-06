# -*- coding: utf-8 -*-

from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Project

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


@router.get('/api/projects/{id}', response_model=list[schema.ProjectProfile])
def api_projects_get_one(id: int, current_user: User = Depends(get_current_user)):
    pass
