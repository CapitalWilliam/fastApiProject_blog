# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       Capital_Wu
   date：          2023/1/25
-------------------------------------------------
   Change Activity:
                   2023/1/25:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED,tags=['blogs'])
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body,
                           user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
async def destroy(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
async def update(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} not found.")
    blog.update(request.dict())
    db.commit()
    return "updated"


@app.get("/blog", response_model=List[schemas.ShowBlog],tags=['blogs'])
async def show_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,tags=['blogs'])
async def show(blog_id: int, response: Response, db: Session = Depends(get_db)):
    one = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {blog_id} is not available."}
    return one


@app.post("/user",response_model=schemas.ShowUser,status_code=status.HTTP_201_CREATED,tags=['users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser,tags=['users'])
async def show_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    one = db.query(models.User).filter(models.User.id == user_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"User with the id {user_id} is not available."}
    return one
