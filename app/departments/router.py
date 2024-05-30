# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import Department

from app.auth import get_current_user
from app.departments import schema

router = APIRouter(tags=['departments'])
