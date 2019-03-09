# -*- coding: utf-8 -*-
"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from db.orangedb import *
from db.models import *

tooldb=Tooldb()


def login(dic):
    condition="name=%s and password=%s and user_type=%s"
    args=(dic['name'],dic['password'],dic['user_type'])
    objs=tooldb.select_many(User,condition,args)
    if objs:
        return {'status':'ok','msg':'登入成功','user':objs[0].__dict__}
    return {'status':'error','msg':'登入失败'}

def register(dic):
    condition="name=%s and user_type=%s"
    args=(dic['name'],dic['user_type'])

    objs=tooldb.select_many(User,condition,args)
    if objs:
        return {'status':'error','msg':'用户名已存在'}
    u1=User(dic['name'],dic['password'],user_type=dic['user_type'])
    if tooldb.save(u1):
        return {'status':'ok','msg':'注册成功'}
    return {'status':'error','msg':'注册失败'}




