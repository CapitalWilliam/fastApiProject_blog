# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     blog
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


async def show_all_blogs(db):
    blogs = db.query(models.Blog).all()
    return blogs


async def create_one_blog(db, request):
    new_blog = models.Blog(title=request.title,
                           body=request.body,
                           user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


async def delete_one_blog(blog_id, db):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found.")
    blog.delete()
    db.commit()


async def update_one_blog(blog_id, db, request):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found.")
    blog.update(request.dict())
    db.commit()


async def show_one_blog(blog_id, db):
    one = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {blog_id} is not available."}
    return one
