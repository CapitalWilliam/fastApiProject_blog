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

from fastapi import FastAPI
from blog import models
from blog.database import engine

from blog.routers import blog, user, anthentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(anthentication.router)
app.include_router(blog.router)
app.include_router(user.router)
