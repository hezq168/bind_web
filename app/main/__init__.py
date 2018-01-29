#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:22
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : __init__.py
# @Project : bind_web
# @Software: PyCharm
from flask import Blueprint
main = Blueprint('main', __name__)

from . import errors,views

