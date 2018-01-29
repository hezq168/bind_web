#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 10:25
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : views.py
# @Project : bind_web
# @Software: PyCharm
from datetime import datetime
from flask import render_template,request,jsonify,abort
from flask_login import login_required, current_user
from . import user
from app.models import User
from app import db
from hashlib import md5
from app.log import log

@user.route('/')
@user.route('/list/')
@login_required
def list():
    # 取出所有用户数据
    _user = User.query.filter_by().all()
    return render_template('user/user.html',users=_user)

# 添加用户
@user.route('/add_user/',methods=['post'])
@login_required
def add_user():
    # 检查是否为ajax请求
    if request.method == 'POST':
        username = request.form.get('add_username', u'无用户名')
        pwd = request.form.get('add_password', u'无密码')
        name = request.form.get('add_name', u'无密码')
        sex = request.form.get('add_sex','')
        qq = request.form.get('add_qq','')
        email = request.form.get('add_email', u'无邮箱')
        tel = request.form.get('add_tel','')
        if username and pwd:
            _user = User(username=username, password=md5(pwd).hexdigest(), name=name,email=email, sex=sex,tel=tel,
                         qq=qq, login_date=datetime.now())
            db.session.add(_user)
            db.session.commit()
            logs = '添加用户%s' %(name)
            log('user',current_user.name,logs,datetime.now(),request.remote_addr)
            msg = {'status': 'ok', 'title': '添加用户', 'txt': '添加用户成功' }
            return jsonify(msg)
        else:
            msg = {'status': 'error', 'title': '添加用户', 'txt': '添加用户失败' }
            return jsonify(msg)
    else:
        abort(403)

# 用户状态修改
@user.route('/user_status/',methods=['get'])
@login_required
def user_status():
    if request.is_xhr:
        uid = request.args.get('user_id')
        ustatus = int(request.args.get('user_op'))
        u = User.query.filter_by(id=uid).first()
        #  ustatus 1 表示激活，0 表示禁用
        if ustatus == 1:
            u.status = 1
            db.session.commit()
            logs = '激活用户：%s' %(u.name)
            log('user',current_user.name,logs,datetime.now(),request.remote_addr)
            msg = {'status':'ok','title':'激活用户','txt':'激活成功'}
            return jsonify(msg)
        else:
            u.status = 0
            db.session.commit()
            logs = '禁用用户：%s' %(u.name)
            log('user',current_user.name,logs,datetime.now(),request.remote_addr)
            msg = {'status':'ok','title':'禁用用户','txt':'禁用成功'}
            return jsonify(msg)
    else:
        abort(403)

# 修改用户
@user.route('/edit_user/',methods=['get','post'])
@login_required
def edit_user():
    if request.method == 'GET'and request.is_xhr:
        user_id = request.args.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        return jsonify(user.to_json())
    elif request.method == 'POST'and request.is_xhr:
        edit_id = request.form.get('edit_id')
        edit_username = request.form.get('edit_username')
        edit_name = request.form.get('edit_name')
        edit_sex = request.form.get('edit_sex')
        edit_tel = request.form.get('edit_tel')
        edit_qq = request.form.get('edit_qq')
        edit_email = request.form.get('edit_email')
        _update = {"username":edit_username,"name":edit_name,"sex":edit_sex,"tel":edit_tel,"qq":edit_qq,
                   "email":edit_email}
        User.query.filter_by(id=edit_id).update(_update)
        db.session.commit()
        logs = '更新用户 %s'  %(_update)
        log('user',current_user.name,logs,datetime.now(),request.remote_addr)
        msg = {'status': 'ok', 'title': '更新用户', 'txt': '更新用户成功' }
        return jsonify(msg)
    else:
        abort(403)


# 添加用户时检查用户名
@user.route('/check_user/', methods=['get'])
@login_required
def check_user():
    if request.is_xhr:
        username = User.query.filter_by(username=request.args.get('add_username','').lower()).first()
        return jsonify(username is None)
    else:
        abort(403)

# 添加用户时检查邮箱
@user.route('/check_email/', methods=['get'])
@login_required
def check_email():
    if request.is_xhr:
        email = User.query.filter_by(email=request.args.get('add_email','').lower()).first()
        return jsonify(email is None)
    else:
        abort(403)
