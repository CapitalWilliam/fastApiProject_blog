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

from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(blog_id, db: Session = Depends(get_db)):
    one = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    db.commit()
    return 'done'



@app.get("/blog")
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
async def show(blog_id: int, response: Response, db: Session = Depends(get_db)):
    one = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {blog_id} is not available."}
    return one
