# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.db import db
from app.models import User, Work

from app.auth import get_current_user
from app.works import schema

router = APIRouter(tags=['works'])
