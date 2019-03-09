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
import os,json,struct
from conf import settings
from threading import Thread

tooldb=Tooldb()
unknown_error={'status':'error','msg':'系统繁忙,请重试'}

def send_notice(dic):
    notice=Notice(dic['title'],dic['content'],dic['user_id'])
    if tooldb.save(notice):
        return {'status':'ok','msg':'公告已发送成功'}
    return

def get_all_user(dic):
    users=tooldb.select_many(User,condition='user_type=0')
    response={'users':[i.__dict__ for i in users]}
    return response

def lock_user(dic):
    u=tooldb.get(User,dic['user_id'])
    u.locked=1
    if tooldb.update(u):
        return {'status':'ok','msg':'锁定成功'}
    return unknown_error

def unlock_user(dic):
    u=tooldb.get(User,dic['user_id'])
    u.locked=0
    if tooldb.update(u):
        return {'status':'ok','msg':'解锁成功'}
    return unknown_error


def check_movie(dic):
    md5=dic['MD5']
    ms=tooldb.select_many(Movie,'MD5=%s',(md5,))
    if ms:
        return {'status':'error','msg':'文件已经存在'}
    return {'status':'ok','msg':'服务器准备接受文件'}

def upload_movie(dic):

    client=dic['client']
    size=dic['size']
    name=dic['name']
    MD5=dic['MD5']
    user_id=dic['user_id']
    isvip=dic['isvip']


    if not os.path.exists(settings.MOVIE_PATH):
       os.mkdir(settings.MOVIE_PATH)
    path=os.path.join(settings.MOVIE_PATH,name)

    def task():
        f=open(path,'wb')
        receive_size=0
        while receive_size<size:
            if receive_size-size<1024:
               data=client.recv(size-receive_size)
            else:
               data=client.recv(1024)
            receive_size+=len(data)
            f.write(data)

        #将数据存储到数据库中

        m=Movie(name,user_id,size,path,MD5,isvip)


        res=tooldb.save(m)
        f.close()
        if res:
            #等待该连接完成上传工作后,再把连接添加到监听列表中
            dic['rlist'].append(client)
            json_bytes = json.dumps({"status":"ok","msg":"上传成功!"}).encode('utf-8')
            len_bytes = struct.pack('i', len(json_bytes))
            client.send(len_bytes)
            client.send(json_bytes)
        else:
            dic['rlist'].append(client)
            json_bytes = json.dumps({'status':'error','msg':'系统繁忙,请重试'}).encode('utf-8')
            len_bytes = struct.pack('i', len(json_bytes))
            client.send(len_bytes)
            client.send(json_bytes)

    #开始线程去处理上传
    Thread(target=task).start()


def get_movies(dic):
    movies=tooldb.select_many(Movie)
    return {'status':'ok','movies':[i.__dict__ for i in movies] if movies else []}


def delete_movie(dic):
    movie=tooldb.get(Movie,dic['id'])
    if tooldb.delete(movie):
        #从文件夹中删除文件
        os.remove(movie.path)
        return {'status':'ok'}
    return unknown_error