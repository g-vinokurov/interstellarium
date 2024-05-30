# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Group, Project

from app.auth import get_current_user
from app.projects import schema

router = APIRouter(tags=['projects'])


@router.post('/api/projects', response_model=list[schema.Project])
def get_projects(
    filters: schema.ProjectFilters,
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
    query = query.join(User, User.id == Project.chief_id, isouter=True)
    query = query.join(Group, Group.id == Project.group_id, isouter=True)
    if filters.name is not None and len(filters.name) != 0:
        query = query.filter(Project.name.ilike(f'%{filters.name}%'))
    if filters.start_date is not None:
        query = query.filter(Project.start_date >= filters.start_date)
    if filters.finish_date is not None:
        query = query.filter(Project.finish_date <= filters.finish_date)

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


@router.post('/api/projects/create', response_model=schema.CreateProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    request: schema.CreateProjectRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )

    with db.Session() as session:
        project = session.execute(
            select(Project).filter_by(name=request.name)
        ).scalar_one_or_none()

    if project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Project exists'
        )

    if request.finish_date and request.start_date:
        if request.start_date > request.finish_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Start date cannot be greater than finish date'
            )

    project = Project()
    project.name = request.name
    project.start_date = request.start_date
    project.finish_date = request.finish_date

    with db.Session() as session:
        session.add(project)
        session.commit()

        project_id = project.id

    item = {'id': project_id}
    return JSONResponse(item, status_code=status.HTTP_201_CREATED)
