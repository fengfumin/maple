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
import os,sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core import admin,user

if __name__ == '__main__':
    funcs={'1':admin.admin_view,'2':user.user_view}
    while True:
        print('''
1.管理员界面
2.用户界面
        ''')
        choise=input('请选择(q退出)>>>:')
        if choise=='q':
            break
        if choise in funcs:
            funcs[choise]()
        else:
            print('输入错误')
    
