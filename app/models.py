#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:26
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : models.py
# @Project : bind_web
# @Software: PyCharm
from . import login_manager, db
from flask_login import UserMixin


# 用户表
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))   # 用户名
    password = db.Column(db.String(64))   # 密码
    name = db.Column(db.String(32))       # 姓名
    login_date = db.Column(db.DateTime())  # 最后一次登录日期
    sex = db.Column(db.String(64))
    qq = db.Column(db.String(64))
    email = db.Column(db.String(64))
    tel = db.Column(db.String(255))
    status = db.Column(db.Integer, default=1)      #用户状态 1:激活  0:禁用

    def __repr__(self):
        return '<username %r>' % (self.name)

    def to_json(self):
        return dict(id=self.id,username=self.username,sex=self.sex,name=self.name,qq=self.qq,
                    email=self.email,tel=self.tel)


# DNS表
class  Dns(db.Model):
    __tablename__ = 'dns_records'
    id = db.Column(db.Integer, primary_key=True)
    zone = db.Column(db.String(255), nullable=False)    # 域名
    host = db.Column(db.String(255), default='@')    # 记录名称
    type = db.Column(db.String(255), nullable=False)    # 记录类型
    data = db.Column(db.String(255))    # 记录值
    ttl = db.Column(db.Integer, nullable=False)        # 过期时间
    view = db.Column(db.String(32), default='DF')      # 视图
    mx_priority = db.Column(db.String(255))
    refresh = db.Column(db.Integer)
    retry = db.Column(db.Integer)
    expire = db.Column(db.Integer)
    minimum = db.Column(db.Integer)
    serial = db.Column(db.Integer)
    resp_person = db.Column(db.String(255))
    primary_ns = db.Column(db.String(255))
    status = db.Column(db.Integer, default=1)  # 域名状态 1：激活  0：禁用

    def __repr__(self):
        return '<zone %r>' % (self.zone)

# log表
class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(32))
    zone = db.Column(db.String(255))    # 域名
    type = db.Column(db.String(16))     # 日志类型login,logout,domain_add,domain_del,domain_edit
    logs = db.Column(db.String(255))
    ip = db.Column(db.String(255))
    date = db.Column(db.DATETIME)

    def __repr__(self):
        return '<zone %r>' % (self.zone)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))