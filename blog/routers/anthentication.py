# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     anthentication
   Description : a router file for anthentication
   Author :       Capital_Wu
   date：          2023/1/26
-------------------------------------------------
   Change Activity:
                   2023/1/26:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from fastapi import APIRouter, status, Depends, HTTPException
from blog import schemas, models
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.hashing import Hash

router = APIRouter(
    prefix="/login",
    tags=['Login']
)


@router.post("/")
async def login(request: schemas.Login,
                db: Session = Depends(get_db),
                ):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        # pass
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invalid Credentials")
    if not Hash.verify(user.password, request.password):
        # pass
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password")
    return user
