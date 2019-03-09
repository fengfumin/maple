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

def login(user_type=0):
    while True:
        name = input('请输入登入用户名>>>:')
        if name == 'q':
            break
        password = input('请输入登入密码>>>:')
        if name and password:
            data = {'name': name,
                    'password': password,
                    'type': 'common',#判断调用哪个接口模块
                    'user_type':user_type,#判断是管理员还是用户
                    'method':'login'}
            response = TCPclient.request(data)

            if response['status'] == 'ok':
                print('登入成功')
                return response
            else:
                print(response['msg'])

        else:
            print('输入错误')
def register(user_type=0):
    while True:
        name=input('请输入注册用户名>>>:')
        if name=='q':
            break
        password=input('请输入注册密码>>>:')
        if name and password:
            data={'name':name,
                  'password':password,
                  'type':'common',
                  'user_type':user_type,
                  'method':'register'}
            response=TCPclient.request(data)

            if response['status']=='ok':
                print('注册成功')
                break
            else:
                print(response['msg'])

        else:
            print('输入错误')