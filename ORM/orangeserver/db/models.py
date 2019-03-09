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
from db.orangedb import MyMetaclass,Field

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

class Movie(metaclass=MyMetaclass):
    id = Field('id', 'int', pri_key=True, increment=True)
    name = Field('name', 'char(20)')
    user_id = Field('user_id', 'int')
    up_time= Field('up_time', 'timestamp')
    MD5= Field('MD5', 'char(50)')
    size = Field('size', 'int')
    path = Field('path', 'varchar(100)')
    isvip = Field('isvip', 'tinyint', default=0)

    def __init__(self,name,user_id,size,path,MD5,isvip=0):
        self.name=name
        self.user_id=user_id
        self.isvip=isvip
        self.size=size
        self.path=path
        self.MD5=MD5


class Notice(metaclass=MyMetaclass):
    id = Field('id', 'int', pri_key=True, increment=True)
    title = Field('title', 'varchar(100)')
    content = Field('content', 'varchar(1000)')
    send_time = Field('send_time', 'timestamp')
    user_id = Field('user_id', 'int')

    def __init__(self,title,content,user_id):
        self.title=title
        self.content=content
        self.user_id=user_id

class ViewRecord(metaclass=MyMetaclass):
    id = Field('id', 'int', pri_key=True, increment=True)
    user_id = Field('user_id', 'int')
    movie_id = Field('movie_id', 'int')
    view_time= Field('view_time', 'timestamp')

    def __init__(self,user_id,movie_id):
        self.user_id=user_id
        self.movie_id=movie_id




