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

from fastapi import HTTPException
from starlette import status

from blog import models
from blog.hashing import Hash


async def create_one_user(db, request):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def show_one_user(db, user_id):
    one = db.query(models.User).filter(models.User.id == user_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"User with the id {user_id} is not available."}
    return one
