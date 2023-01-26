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

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from blog import schemas, models
from blog.database import get_db
from blog.hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, )
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, )
async def show_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    one = db.query(models.User).filter(models.User.id == user_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"User with the id {user_id} is not available."}
    return one
