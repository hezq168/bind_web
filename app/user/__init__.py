#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 10:24
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : __init__.py.py
# @Project : bind_web
# @Software: PyCharm
from flask import Blueprint
user = Blueprint('user', __name__)

from . import views