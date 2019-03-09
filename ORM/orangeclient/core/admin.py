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
import hashlib
import os,json,struct

user=None

def user_auth(func):
    def wrapper(*args,**kwargs):
        if not user:
            print('请先登入')
            login()
            if user:
                return func(*args,**kwargs)
        else:
            return func(*args,**kwargs)
    return wrapper

def get_MD5(path):
    size=os.path.getsize(path)
    f=open(path,'rb')
    m=hashlib.md5()
    if size<1024*1024:
        m.update(f.read())
    else:
        data1=f.read(1024)
        f.seek(-1024,2)
        data2=f.read(1024)
        f.seek(size//2,0)
        data3=f.read(1024)
        m.update(data1)
        m.update(data2)
        m.update(data3)
    return m.hexdigest()


def login():
   response=common.login(1)
   if response:
        global user
        user=response['user']
def register():
    response=common.register(1)

@user_auth
def send_notice():
    while True:
        title=input('请输入标题>>>:')
        if title=='q':
            return
        if not title:
            print('标题不能为空')
            continue
        content=input('请输入内容>>>:')
        if not content:
            print('内容不能为空')
            continue
        request_data={'title':title,
                      'content':content,
                      'user_id':user['id'],
                      'type':'admin',
                      'method':'send_notice'}
        dic=TCPclient.request(request_data)
        print(dic['msg'])
        return

@user_auth
def lock_user():
    request_data={'type':'admin',
                  'method':'get_all_user'}
    response=TCPclient.request(request_data)
    for u in response['users']:
        print('%s %s %s'%(u['id'],u['name'],u['locked']))
    id=int(input('请选择要锁定账户编号>>>:'))

    if id in [u['id'] for u in response['users']]:
        #根据id获取用户
        for u in response['users']:
            if u['id']==id:
                #判断这个用户的锁定状态
                if u['locked']==1:
                    print('该账户已经锁定')
                    break
        else:
            response_data={'type':'admin','method':'lock_user','user_id':id}
            response=TCPclient.request(response_data)
            print(response)
    else:
        print('输入id不正确')

@user_auth
def unlock_user():
    request_data = {'type': 'admin',
                    'method': 'get_all_user'}
    response = TCPclient.request(request_data)
    for u in response['users']:
        print('%s %s %s' % (u['id'], u['name'], u['locked']))
    id = int(input('请选择要解锁账户编号>>>:'))

    if id in [u['id'] for u in response['users']]:
        # 根据id获取用户
        for u in response['users']:
            if u['id'] == id:
                # 判断这个用户的锁定状态
                if u['locked'] == 0:
                    print('该账户未锁定')
                    break
        else:
            response_data = {'type': 'admin', 'method': 'unlock_user', 'user_id': id}
            response = TCPclient.request(response_data)
            print(response)
    else:
        print('输入id不正确')
    pass

@user_auth
def upload_movie():
    while True:
        # filepath=input('请输入上传文件路径>>>:').strip()
        filepath = r'D:\上海python全栈4期\day53\视频\1.youku系统回顾.mp4'
        if not os.path.exists(filepath):
            print('对不起:路径不存在!')
            continue

        if not os.path.isfile(filepath):
            print('对不起:只能上传文件')
            continue
        suffixs=['mp4','mkv','mov','rmvb','avi']
        if not filepath.split('.')[-1] in suffixs:
            print('文件格式不支持!')
            continue
        md5=get_MD5(filepath)
        request_data = {'type': 'admin', 'method': 'check_movie','MD5':md5,
                     }
        response=TCPclient.request(request_data)
        break

    if response['status']=='ok':
        print(response['msg'])
        #文件名
        name=(os.path.split(filepath)[-1])
        #文件后缀名
        size=os.path.getsize(filepath)

        vip=input('请输入该视频是否收费,y收费,其他免费').strip().lower()
        if vip=='y':
            vip=1
        else:
            vip=0
        print('开始上传文件:%s'%name)


        #先发送文件信息
        file_info={'name':name,
                   'size':size,
                   'MD5':md5,
                   'user_id':user['id'],
                   'isvip':vip,
                   'type':'admin',
                   'method':'upload_movie'}
        # 字典转json再转二进制
        json_bytes = json.dumps(file_info).encode('utf-8')
        # 获取数据长度
        len_bytes = struct.pack('i', len(json_bytes))
        TCPclient.conn.send(len_bytes)
        TCPclient.conn.send(json_bytes)

        #上传文件
        f=open(filepath,'rb')
        send_size=0
        while send_size<size:
            data=f.read(1024)
            TCPclient.conn.send(data)
            send_size+=len(data)
            print('上传了%s%s'%((send_size/size)*100,'%'))
        print('上传完毕')
        #接受上传结果
        len_data = TCPclient.conn.recv(4)
        len_bytes = struct.unpack('i', len_data)[0]
        json_data = TCPclient.conn.recv(len_bytes).decode('utf-8')
        dic = json.loads(json_data)
        print(dic['msg'])
    else:
        print(response['msg'])



@user_auth
def delete_movie():
    request_data={'type':'admin','method':'get_movies'}
    response=TCPclient.request(request_data)
    if not response['movies']:
        print('没有任何视屏')
        return
    ids=[d['id'] for d in response['movies']]
    for m in response['movies']:
        print('id:%s name:%s'%(m['id'],m['name']))
    while True:
        id=int(input('请输入要删除的ID>>>:').strip())
        if id in ids:
            reqyest_data={'type':'admin',
                         'method':'delete_movie',
                          'id':id}
            response=TCPclient.request(request_data)
            if response['status']=='ok':
                print('删除成功')
                return
            else:
                print(response['msg'])
                return
        else:
            print('id输入错误')


def admin_view():
    funcs={'1':login,'2':register,'3':send_notice,'4':lock_user,'5':unlock_user,
           '6':upload_movie,'7':delete_movie}
    while True:
        print('''
1.登录
2.注册
3.发布公告
4.解锁账户
5.锁定账户
6.上传视频
7.删除视频 
        ''')
        choise=input('请选择(q退出)>>>:')
        if choise=='q':
            break
        if choise in funcs:
            funcs[choise]()
        else:
            print('输入错误')

if __name__ == '__main__':
    upload_movie()
