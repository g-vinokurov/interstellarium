# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.departments.router import router as departments_router
from app.contracts.router import router as contracts_router
from app.projects.router import router as projects_router
from app.equipment.router import router as equipment_router
from app.groups.router import router as groups_router
from app.works.router import router as works_router

app = FastAPI()

# TODO: it must be configured more carefully
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(departments_router)
app.include_router(contracts_router)
app.include_router(projects_router)
app.include_router(equipment_router)
app.include_router(groups_router)
app.include_router(works_router)


if __name__ == '__main__':
    pass
