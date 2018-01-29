#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 17:18
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : log.py
# @Project : bind_web
# @Software: PyCharm

from app.models import Log
from app import db


# 日志函数
def log(type,user,logs,date,ip,zone=None):
    '''
    type 类型
    login,logout,
    user
    domain '''
    _log = Log(type=type,user=user,logs=logs,date=date,ip=ip,zone=zone)
    try:
        db.session.add(_log)
        db.session.commit()
    except:
        pass
