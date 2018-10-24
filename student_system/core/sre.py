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
import json
from conf import setting

#学生类
class Student:
    # 初始化姓名,年龄,语文,数学,英文
    def __init__(self,name,age,chinese,math,english):
        self.name=name
        self.age=age
        self.chinese=chinese
        self.math=math
        self.english=english
    #自我介绍功能
    def say_self(self):
        print('姓名:%-10s 年龄:%-10s 语文:%-10s 数学:%-10s 英文:%-10s'%\
              (self.name,self.age,self.chinese,self.math,self.english))


#学生管理类
class StudentManger:
    def __init__(self,students):
        self.students=students
    #根据姓名查看学生所有的学科
    def show_score_with_name(self):
        while True:
            name=input('请输入姓名:')
            if name=='q':return
            if not name:
                print('不能为空')
                continue
            for s in self.students:
                if s.name==name:
                    s.say_self()
                    return
            else:
                print('没有这个人')
                continue
    #查看所有人的某学科成绩
    def show_score_with_subject(self):
        while True:
            subject=input('请输入学科:')
            if subject == 'q': return
            if not subject:
                print('不能为空')
                continue
            for s in self.students:
                print('姓名:%s %s:%s'%(s.name,subject,s.__dict__[subject]))
                return
            else:
                print('没有这个学科')
                continue

    #查看总平均分
    def show_avarage(self):
        score_sum=0
        for s in self.students:
            score_sum+=s.english
            score_sum+=s.math
            score_sum+=s.chinese
        print('平均分为:%s'%(score_sum/(len(self.students)*3)))


    #查看某的某学科成绩
    def show_score_with_subject_name(self):
        while True:
            subject=input('请输入学科:')
            if subject == 'q': return
            if not subject:
                print('不能为空')
                continue
            if subject in ['chinese','math','english']:
                name=input('请输入姓名:')
                if name == 'q': return
                if not name:
                    print('不能为空')
                    continue
                for s in self.students:
                    if s.name==name:
                        print('姓名:%s %s:%s'%(s.name,subject,s.__dict__[subject]))
                        return
                else:
                    print('没有这个同学')
                    continue
            else:
                print('没有这个学科')
                continue

    #根据姓名删除学生信息
    def delete_student(self):
        while True:
            name=input('输入要删除的姓名:')
            if name=='q':return
            if not name:
                print('不能为空')
                continue
            for s in self.students:
                if s.name==name:
                    self.students.remove(s)
                    print('删除成功')
                    save_data(self.students)
                    return
            else:
                print('没有这个人')
                continue

def user_view():
    print('欢迎使用学员管理系统')
    #创建管理器对象
    manager=StudentManger(load_data())

    funcs={'1':manager.show_score_with_name,
           '2':manager.show_score_with_subject,
           '3':manager.show_avarage,
           '4':manager.show_score_with_subject_name,
           '5':manager.delete_student}

    while True:
        print('''
1.根据姓名查看学生所有成绩
2.查看所有人的某学科成绩
3.查看总平均分
4.查看某人的某学科成绩
5.根据姓名删除学生信息
输入q退出''')
        res=input('请选择功能:')
        if res=='q':
            print('你已退出系统')
            return
        if res in funcs:
            funcs[res]()
        else:
            print('错误指令,请重试!')

#解析json数据,转换为学生对象,返回存储学生对象的数组
def load_data():
    stus=[]
    f=open(setting.JSON_PATH,'r',encoding='utf-8')
    #解析json数据
    dic=json.load(f)
    for s in dic['stus']:
        #转换为学生对象
        stu=Student(s['name'],s['age'],s['chinese'],s['math'],s['english'])
        stus.append(stu)
    f.close()
    return stus

#将内存中的对象解析后dump到json文件中
def save_data(students):
    dic={'auth':'maple','stus':{}}
    f=open(setting.JSON_PATH,'w',encoding='utf-8')
    #序列化json数据
    stus=[]
    for i in students:
        stu = {}
        stu['name']=i.name
        stu['age']=i.age
        stu['english']=i.english
        stu['math']=i.math
        stu['chinese']=i.chinese
        stus.append(stu)
    dic['stus'] = stus
    json.dump(dic,f,ensure_ascii=False)
    f.close()











