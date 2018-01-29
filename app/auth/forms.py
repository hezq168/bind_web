#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:54
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : forms.py
# @Project : bind_web
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Required,Length


# 用户登录from
class LoginFrom(FlaskForm):
    username = StringField('用户名：', validators=[Required(),Length(1,8,message=u"用户名长度不正确")],render_kw={"placeholder": "用户名",})
    password = PasswordField('密码：', validators=[Required()],render_kw={"placeholder": "密码",})
    submit = SubmitField('登录')