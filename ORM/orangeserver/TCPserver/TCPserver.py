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
import struct
import socket
import json
from core import user_interface,admin_interface,common_interface
import select

rlist = []

def start_server():
    server = socket.socket()
    server.bind(('127.0.0.1', 8888))
    server.listen(5)
    rlist.append(server)
    # 多路复用设置
    wlist = []
    while True:
        # 1指定超时时间,不指定就不会超时,意思是超过1秒后,不再监听当前的连接
        readable,writeable,_=select.select(rlist,wlist,[],1)
        for r in readable:
            if r==server:
                conn,addr=server.accept()
                rlist.append(conn)
            else:
                working(r)


def working(client):
        try:
            len_bytes=client.recv(4)
            if not len_bytes:
                return
        except Exception as e:
            client.close()
            rlist.remove(client)
            print(e)
            return

        len_data=struct.unpack('i',len_bytes)[0]
        json_data=client.recv(len_data).decode('utf-8')
        dic=json.loads(json_data)
        dic['client'] = client
        if dic['method']=='upload_movie':
            dic['rlist']=rlist
            #连接让upload_movie的子线程去执行,把该连接从监听列表中删除
            rlist.remove(client)

        #封装admin,user,common三个模块的interface接口
        type_funcs={'user':user_interface.__dict__,
                    'admin':admin_interface.__dict__,
                    'common':common_interface.__dict__ }
        if dic['type'] in type_funcs:
            if dic['method'] in type_funcs[dic['type']]:
                response=type_funcs[dic['type']][dic['method']](dic)
            else:
                response={"status":"error","msg":"没有这个功能!"}
        else:
            print('请求类型错误,请检查type字段')

        if dic['method']=='upload_movie':
            return
        json_bytes=json.dumps(response).encode('utf-8')
        len_bytes=struct.pack('i',len(json_bytes))
        client.send(len_bytes)
        client.send(json_bytes)





            
    











