#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:18
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : run.py
# @Project : bind_web
# @Software: PyCharm
from app import create_app, db
from app import models
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()