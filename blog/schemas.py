# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     schemas
   Description :
   Author :       Capital_Wu
   date：          2023/1/25
-------------------------------------------------
   Change Activity:
                   2023/1/25: 使用pydantic 创建
-------------------------------------------------
schemas在后端中通常指数据库架构。

数据库架构是指数据库结构的定义，包括数据库中表、字段、关系、约束等。在设计数据库架构时，需要考虑数据的存储、检索和维护的需求。

例如，在一个电商网站中，可能需要存储用户信息，订单信息和商品信息。用户信息可能包括用户名、电子邮件地址、密码等字段。订单信息可能包括订单编号、用户ID、商品ID等字段。商品信息可能包括商品名称、价格、库存等字段。

另一个例子是在一个社交网站中，可能需要存储用户信息，好友关系和帖子信息。用户信息可能包括用户名、电子邮件地址、密码等字段。好友关系可能包括用户ID、好友ID等字段。帖子信息可能包括帖子ID、用户ID、帖子内容等字段。

在这两个例子中，schemas就指的是表、字段、关系、约束等数据库架构。
"""
__author__ = 'Capital_Wu'

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
