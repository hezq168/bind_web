#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:18
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : config.py
# @Project : bind_web
# @Software: PyCharm
import os
basedir = os.path.abspath(os.path.dirname(__file__))




class Config():
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    CSRF_ENABLED = True
    SECRET_KEY = 'asdfaaadwerb42435bvvq1234a801faaa1123sdfac31*'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
#   mysql自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
#   mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xxx:xxxx@127.0.0.1/dns?charset=utf8'
#   打印sql
    SQLALCHEMY_ECHO = True



#   DNS分页
    POSTS_PER_PAGE = 15
#   DNS类型
    DNS_TYPE = ['A', 'NS', 'CNAME']
#   DNS NS记录
    DNS_NS = ['ns1.xxxx.com', 'ns2.xxxx.com']
#   DNS线路
    DNS_VIEW = {'DF': '默认', 'CNC': '联通', 'CT': '电信'}
#   DNS TTL
    DNS_TTL = [60, 10, 600]
#   DNS SOA
    SOA = {'refresh':3600,'retry':180, 'expire':1209600, 'minimum':180,' resp_person':'root.xxxx.com.','primary_ns':'ns1.xxxx.com.'}




    @staticmethod
    def init_app(app):
        pass
