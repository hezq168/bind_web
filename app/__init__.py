#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:18
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : __init__.py
# @Project : bind_web
# @Software: PyCharm
# -*- coding:utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

from config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
config = Config()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = None
sess = Session()




# 程序初始化
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  #csf

    bootstrap.init_app(app)
    db.init_app(app)
    config.init_app(app)
    sess.init_app(app)
    login_manager.init_app(app)

    #  登录蓝图
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # 主蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 用户蓝图
    from .user import user as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/user')


    return app