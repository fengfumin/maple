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

from TCPclient import TCPclient
from core import common
import os,json,struct
from conf import settings
user=None

def user_auth(func):
    def wrapper(*args,**kwargs):
        if not user:
            print('请先登入')
            login()
            if user:
                return func(*args,**kwargs)
        return func(*args,**kwargs)
    return wrapper


def login():
   response=common.login(0)
   if response:
       global user
       user=response['user']

def register():
    response=common.register(0)

@user_auth
def open_vip():
    if user['isvip']==1:
        print('你已经是会员了!')
        return
    res=(input('请支付100元开通vip会员,是否确认Y,输入其他取消')).lower()
    if res=='y':
        request_data={'type':'user',
                      'method':'open_vip',
                      'user_id':user['id']}
        response=TCPclient.request(request_data)
        print(response['msg'])
    else:
        print('操作错误')


@user_auth
def show_movies():
    request_data = {'type': 'admin',
                    'method': 'get_movies'}
    response = TCPclient.request(request_data)
    for m in response['movies']:
        print('序号:%s 电影名:%s 件大小:%s'%(m['id'],m['name'],m['size']))
    return response
@user_auth
def download_movie():
    response=show_movies()
    if not response:
        return
    ids=[m['id'] for m in response['movies']]
    id=input('请输入你要下载的电影序号>>>:')
    if id=='q':
        return
    if not id.isdigit():
        print('输入不正确')
        return
    id=int(id)
    if id not in ids:
        print('输入不正确')
        return
    #接收文件,取出文件信息
    movie=None
    for m in response['movies']:
        if m['id']==id:
            movie=m
    if not os.path.exists(settings.MOVIE_PATH):
        os.mkdir(settings.MOVIE_PATH)

    #判断本地是否存在这个文件
    path=os.path.join(settings.MOVIE_PATH,movie['name'])
    if os.path.exists(path):
        print('文件已经下载')
        return
    #判断是否可以下载
    request_data={'type':'user','method':'check_download','movie_id':id,'user_id':user['id']}
    response=TCPclient.request(request_data)
    if response['status']!='ok':
        print(response['msg'])
        return


    #添加属性,调用服务端download_movie下载
    request_data['method']='download_movie'
    json_bytes = json.dumps(request_data).encode('utf-8')
    # 获取数据长度
    len_bytes = struct.pack('i', len(json_bytes))
    TCPclient.conn.send(len_bytes)
    TCPclient.conn.send(json_bytes)

    name=movie['name']
    size=movie['size']
    receive_size=0
    f=open(path,'wb')
    while receive_size<size:
        if size-receive_size<1024:
            data=TCPclient.conn.recv(size-receive_size)
        else:
            data=TCPclient.conn.recv(1024)
        receive_size+=len(data)
        print('下载了%s%s' % ((receive_size / size) * 100, '%'))
        f.write(data)
    f.close()
    print('下载完成')


@user_auth
def show_record():
    request_data={
        'type':'user',
        'method':'show_record',
        'user_id':user['id']
    }
    response=TCPclient.request(request_data)
    if not response:
        print('还没有下载记录')
        return
    # print(response)
    # {'records': [{'id': 1, 'user_id': 3, 'movie_id': 1, 'view_time': '2018-12-09 18:34:25'}]}
    for n in response['records']:
        for m in response['movies']:
            print('电影名称:%s ,下载时间:%s'%(m['name'],n['view_time']))

@user_auth
def show_notice():
    request_data={'type':'user',
                  'method':'show_notice' }
    response=TCPclient.request(request_data)
    for n in response['notices']:
        print('========%s========'%n['title'])
        print(n['content'])
        print('========%s========'%n['send_time'])


def user_view():
    funcs={'1':login,'2':register,'3':open_vip,'4':show_movies,'5':download_movie,
           '6':show_record,'7':show_notice}
    while True:
        print('''
1.登入
2.注册
3.开会员
4.查看视频
5.下载视频 
6.查看浏览记录
7.查看公告
        ''')
        choise=input('请选择(q退出)>>>:')
        if choise=='q':
            break
        if choise in funcs:
            funcs[choise]()
        else:
            print('输入错误')
