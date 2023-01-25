# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     hashing
   Description :
   Author :       Capital_Wu
   date：          2023/1/26
-------------------------------------------------
   Change Activity:
                   2023/1/26:
-------------------------------------------------
"""
__author__ = 'Capital_Wu'

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        hashed_password = pwd_context.hash(password)
        return hashed_password
