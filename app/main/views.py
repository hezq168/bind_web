#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 16:25
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : views.py
# @Project : bind_web
# @Software: PyCharm
from datetime import datetime
from flask import render_template,request,jsonify,abort
from flask_login import login_required, current_user
from . import main
# 引入models模型
from app.models import Dns,Log
from app import db
# 引入日志模块
from app.log import log
from app import config

# 域名列表
@main.route('/')
@login_required
def index():
    dns = Dns.query.filter_by(type='SOA').all()
    return render_template('main/index.html',dns=dns)

# 检查域名
@main.route('/check_domain/',methods=['GET'])
@login_required
def check_domain():
    if request.is_xhr:
        username = Dns.query.filter_by(zone=request.args.get('add_dom','').lower()).first()
        return jsonify(username is None)
    else:
        abort(403)



# 添加域名
@main.route('/add_domain/',methods=['POST'])
@login_required
def add_domain():
    domain = request.form.get('add_dom')
    serial = datetime.now().strftime('%Y%m%d%S')
    _dns=Dns(zone=domain,host='@',type='SOA',data=config.SOA['primary_ns'],ttl=config.DNS_TTL[-1],refresh=config.SOA['refresh'],
             retry=config.SOA['retry'],expire=config.SOA['expire'],minimum=config.SOA['minimum'],
             resp_person=config.SOA['minimum'],primary_ns=config.SOA['primary_ns'],status=1,serial=serial)
    _d1 = Dns(zone=domain,host='@',type='NS',data=config.DNS_NS[0]+'.',ttl=86400)
    _d2 = Dns(zone=domain,host='@',type='NS',data=config.DNS_NS[1]+'.',ttl=86400)

    try:
        db.session.add(_dns)
        db.session.add(_d1)
        db.session.add(_d2)
        db.session.commit()
        logs='添加域名：%s' %(domain)
        log('domain',current_user.name,logs,datetime.now(),request.remote_addr,zone=domain)
        return jsonify({'status': u'域名添加成功!'})
    except:
        abort(403)


# 删除域名
@main.route('/del_domain/',methods=['POST'])
@login_required
def del_domain():
    if request.is_xhr:
        zone = request.form.get('zone')
        if zone:
            # 批量删除
            Dns.query.filter_by(zone=zone).delete()
            db.session.commit()
            logs='删除域名：%s' %(zone)
            log('domain',current_user.name,logs,datetime.now(),request.remote_addr,zone=zone)
            return jsonify({'status': u'域名删除成功!'})
        else:
            abort(403)
    else:
        abort(403)




# 域名解析列表
@main.route('/domain_list/<zone>')
@login_required
def domain_list(zone):
    domain = Dns.query.filter(Dns.zone==zone).filter(Dns.type!='SOA').all()
    type = config.DNS_TYPE
    view = config.DNS_VIEW
    ttl = config.DNS_TTL
    return render_template('domain/domain.html',domains=domain,type=type,view=view,ttls=ttl)

# 启/停域名解析
@main.route('/domain_status/',methods=['POST'])
@login_required
def domain_status():
    if request.is_xhr:
        id = request.form.get('id')
        val = int(request.form.get('val'))
        if id:
            _dns = Dns.query.filter_by(id=id).first()
            _dns.status = val
            db.session.commit()
            if val == 0:
                logs = '暂停解析:域名%s，主机记录%s' %(_dns.zone,_dns.host)
                msg = {'status': 'ok', 'title': '暂停解析', 'txt': '暂停解析成功','zone':_dns.zone }
            else:
                logs = '启用解析:域名%s，主机记录%s' %(_dns.zone,_dns.host)
                msg = {'status': 'ok', 'title': '启用解析', 'txt': '启用解析成功','zone':_dns.zone }
            log('domain',current_user.name,logs,datetime.now(),request.remote_addr,zone=_dns.zone)
            return jsonify(msg)
        else:
            abort(403)
    abort(403)


# 添加域名解析记录
@main.route('/add_zone/',methods=['POST'])
@login_required
def add_zone():
    if request.is_xhr:
        zone = request.form.get('add_zone')
        host = request.form.get('add_host')
        _type = request.form.get('add_type')
        view = request.form.get('add_view')
        data = request.form.get('add_data')
        ttl = request.form.get('add_ttl')
        if host is None and _type is None and view is None  and data is None and ttl is None and zone is None:
            abort(403)
        else:
            _zone = Dns(zone=zone,host=host,type=_type,view=view,data=data,ttl=ttl,status=1)
            db.session.add(_zone)
            db.session.commit()
            logs= '添加解析：主机记录:%s，记录类型:%s，线路类型:%s，记录值:%s,TTL(秒):%s' %(host, _type, view, data, ttl)
            log('domain',current_user.name,logs,datetime.now(),request.remote_addr,zone=zone)
            msg = {'status': 'ok', 'title': '添加解析', 'txt': '添加解析成功','zone': '/domain_list/'+zone }
            return jsonify(msg)
    else:
        abort(403)


# 删除解析
@main.route('/del_zone/',methods=['POST'])
@login_required
def del_zone():
    if request.is_xhr:
        id = request.form.get('id')
        _dns = Dns.query.filter_by(id=id).first()
        try:
            db.session.delete(_dns)
            db.session.commit()
            logs= '删除解析：主机记录:%s，记录类型:%s，线路类型:%s，记录值:%s,TTL(秒):%s' %(_dns.host, _dns.type,_dns.view, _dns.data, _dns.ttl)
            log('domain',current_user.name,logs,datetime.now(),request.remote_addr,zone=_dns.zone)
            return jsonify({'status': u'删除成功!'})
        except:
            abort(403)
    else:
        abort(403)


# 修改解析
@main.route('/update_zone/',methods=['POST','GET'])
@login_required
def update_zone():
    if request.method == 'GET' and request.is_xhr:
        id = request.args.get('id')
        if id:
            _dns = Dns.query.filter_by(id=id).first()
            _dnss ={'id':_dns.id,'zone':_dns.zone,'host':_dns.host,'type':_dns.type,'data':_dns.data,'ttl':_dns.ttl,'view':_dns.view}
            return jsonify(_dnss)
        else:
            abort(403)
    elif request.method == 'POST' and request.is_xhr:
        id = request.form.get('edit_id')
        zone = request.form.get('edit_zone')
        host = request.form.get('edit_host')
        _type = request.form.get('edit_type')
        view = request.form.get('edit_view')
        data = request.form.get('edit_data')
        ttl = request.form.get('edit_ttl')
        if host is None and _type is None and view is None  and data is None and ttl is None and zone is None:
            abort(403)
        else:
            _dns = Dns.query.filter_by(id=id).first()
            _update = {"zone":zone,"host":host,"type":_type,"view":view,"data":data,"ttl":ttl}
            Dns.query.filter_by(id=id).update(_update)
            db.session.commit()
            logs = '更新解析：原主机记录:%s，原记录类型:%s，原线路类型:%s，原记录值:%s,TTL(秒):%s' %(_dns.host, _dns.type, _dns.view, _dns.data, _dns.ttl)
            _logs= '新主机记录:%s，新记录类型:%s，新线路类型:%s，新记录值:%s,新TTL(秒):%s' %(host, _type, view, data, ttl)
            log('domain',current_user.name,logs+_logs,datetime.now(),request.remote_addr,zone=zone)
            msg = {'status': 'ok', 'title': '添加解析', 'txt': '添加解析成功','zone': '/domain_list/'+zone }
            return jsonify(msg)
    else:
        abort(403)



# 日志
@main.route('/domain_log/',methods=['GET'])
@login_required
def domain_log():
    page = request.args.get('page', 1, type=int)
    pagination = Log.query.order_by(db.desc(Log.id)).paginate(page,per_page=config.POSTS_PER_PAGE,error_out=False)
    posts = pagination.items
    return render_template('main/logs.html',posts=posts,pagination=pagination)