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
import socket
import json
import struct

conn=socket.socket()
conn.connect(('127.0.0.1',8888))

def request(data):
    #字典转json再转二进制
    json_bytes=json.dumps(data).encode('utf-8')
    #获取数据长度
    len_bytes=struct.pack('i',len(json_bytes))
    conn.send(len_bytes)
    conn.send(json_bytes)
    
    #接收数据
    len_data=conn.recv(4)
    len_bytes=struct.unpack('i',len_data)[0]
    json_data=conn.recv(len_bytes).decode('utf-8')
    dic=json.loads(json_data)
    return dic