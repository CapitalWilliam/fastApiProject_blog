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

from fastapi import Depends, APIRouter,status
from sqlalchemy.orm import Session
from blog import schemas
from blog.database import get_db
from blog.repository.blog import show_all_blogs, create_one_blog, delete_one_blog, update_one_blog, show_one_blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.get("/", response_model=List[schemas.ShowBlog],)
async def get_all(db: Session = Depends(get_db)):
    return await show_all_blogs(db)


@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return await create_one_blog(db, request)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT,)
async def destroy(blog_id, db: Session = Depends(get_db)):
    return await delete_one_blog(blog_id, db)


@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED,)
async def update(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    return await update_one_blog(blog_id, db, request)


@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,)
async def show(blog_id: int, db: Session = Depends(get_db)):
    return await show_one_blog(blog_id, db)


