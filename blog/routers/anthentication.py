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
from fastapi.security import OAuth2PasswordRequestForm

from blog import models
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.hashing import Hash
from blog.token import create_access_token

router = APIRouter(
    prefix="/login",
    tags=['Login']
)


@router.post("/")
async def login(request: OAuth2PasswordRequestForm = Depends(),
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

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # data={"sub": user.username}, expires_delta=access_token_expires
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
