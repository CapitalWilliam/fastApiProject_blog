# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     user
   Description :
   Author :       Capital_Wu
   date：          2023/1/26
-------------------------------------------------
   Change Activity:
                   2023/1/26:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from fastapi import Depends, APIRouter,status,Response
from sqlalchemy.orm import Session

from blog import schemas
from blog.database import get_db
from blog.repository.user import create_one_user, show_one_user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, )
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return await create_one_user(db, request)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, )
async def show_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    return await show_one_user(db, user_id)


