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

from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from blog import schemas, models
from blog.database import get_db

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)


@router.get("/", response_model=List[schemas.ShowBlog],)
async def show_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body,
                           user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT,)
async def destroy(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found.")
    blog.delete()
    db.commit()
    return 'done'


@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED,)
async def update(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found.")
    blog.update(request.dict())
    db.commit()
    return "updated"


@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,)
async def show(blog_id: int, response: Response, db: Session = Depends(get_db)):
    one = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {blog_id} is not available."}
    return one
