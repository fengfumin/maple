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
from orangedb import Field,MyMetaclass


#定义一个用户信息类
class User(metaclass=MyMetaclass):
    #创建字段对象
    id=Field('id','int',pri_key=True,increment=True)
    name=Field('name','char(20)')
    password=Field('password','char(20)',default='12345678')
    isvip=Field('isvip','tinyint',default=0)
    locked=Field('locked','tinyint',default=0)
    user_type=Field('user_type','tinyint',default=0)

    def __init__(self,name,password,user_type=0,isvip=0,locked=0):
        self.name=name
        self.password=password
        self.isvip=isvip
        self.locked=locked
        self.user_type=user_type