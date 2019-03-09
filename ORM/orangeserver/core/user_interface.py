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
from threading import Thread

tooldb=Tooldb()
unknown_error={'status':'error','msg':'系统繁忙,请重试'}

def open_vip(dic):
    u=tooldb.get(User,dic['user_id'])
    u.isvip=1
    if tooldb.update(u):
        return {'status':'ok','msg':'恭喜成为会员'}
    return unknown_error

def show_notice(dic):
    notices=tooldb.select_many(Notice)
    return {'notices':[n.__dict__ for n in notices] if notices else []}

def check_download(dic):
    user=tooldb.get(User,dic['user_id'])
    movie=tooldb.get(Movie,dic['movie_id'])
    if user.isvip==1:
        return {'status':'ok','msg':'尊敬的会员,您可以开始下载了'}
    elif user.isvip==0 and movie.isvip==0:
        return {'status':'ok','msg':'免费的拿去看吧,臭屌丝'}
    else:
        return {'status':'error','msg':'对不起,这是收费的'}

def download_movie(dic):
    #先获取视频的信息
    movie=tooldb.get(Movie,dic['movie_id'])
    client=dic['client']

    def task():
        size=movie.size
        send_size=0
        f=open(movie.path,'rb')
        while send_size<size:
            data=f.read(1024)
            client.send(data)
            send_size+=len(data)

    Thread(target=task).start()
    print(dic)
    user_id=dic['user_id']
    movie_id=dic['movie_id']
    record=ViewRecord(user_id,movie_id)
    tooldb.save(record)

def show_record(dic):
    records = tooldb.select_many(ViewRecord,dic['user_id'])
    records_user=[]
    movies=[]
    for r in records:
        if r.user_id==dic['user_id']:
            records_user.append(r)
            moive=tooldb.get(Movie,r.movie_id)
            movies.append(moive)
    if not records_user:
        return


    return {'records':[n.__dict__ for n in records_user] if records_user else [],
           'movies': [n.__dict__ for n in movies] if movies else []}
