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

from fastapi import FastAPI, Depends
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


@app.post("/blog")
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}")
async def show(blog_id: int, db: Session = Depends(get_db)):
    one = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    return one


