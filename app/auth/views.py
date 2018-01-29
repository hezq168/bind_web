#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:24
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : views.py
# @Project : bind_web
# @Software: PyCharm
import sys

from flask_login import login_required, login_user, logout_user,current_user
from flask import render_template, redirect, url_for, flash,request

from . import auth
from .forms import LoginFrom
from ..models import User

# 引入md5
from hashlib import md5
from app.log import log
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

# 用户登录
@auth.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        md5_pw = md5(form.password.data).hexdigest()  #获取用户密码并MD5
        print md5_pw
        # 判断用户状态 1 激活，0 禁用
        if user.status == 1:
            # 判断用户和密码
            if user is not None and user.password == md5_pw:
                login_user(user)
                # 记录日志
                log('login', current_user.name, '登录系统', datetime.now(), request.remote_addr)
                return redirect(url_for('main.index'))
            else:
                flash('用户名或密码错误！！！')
        else:
            flash('用户被禁用，联系管理员处理！')
    return render_template('auth/login.html', form=form)


# 用户退出
@auth.route('/logout')
@login_required
def logout():
    # 记录日志
    log('logout', current_user.name, '退出系统', datetime.now(), request.remote_addr)
    logout_user()
    flash('退出成功')
    return redirect(url_for('auth.login'))