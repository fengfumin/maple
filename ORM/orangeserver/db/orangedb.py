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
import pymysql
import time
from datetime import datetime

#定义一个字段名类,依次是字段名,数据类型,主键,主键自动增长,默认值
class Field:
    def __init__(self,name,column_type,pri_key=False,increment=False,default=None):
        self.name=name
        self.column_type=column_type
        self.pri_key=pri_key
        self.increment=increment
        self.default=default

#定义一个元类,在创建其他表类时,自动生成创表sql语句
class MyMetaclass(type):
    def __init__(self,class_name,bases,namespace):
        table_name=class_name#将类名作为表名
        columns=[]
        #从类的名称空间获取字段信息,拼接成建表语句
        for k,field in namespace.items():
            if isinstance(field,Field):
                fs='%s %s'%(field.name,field.column_type)
                if field.pri_key:
                    fs+=' primary key'
                    self.pri_key=field.name
                if field.increment:
                    fs+=' auto_increment'
                if field.default !=None:
                    if isinstance(field.default,int):
                        fs+=' default %s'%field.default
                    elif isinstance(field.default,str):
                        fs+=" default '%s'"%field.default
                    else:
                        raise TypeError('默认值必须是字符串或整数')
                columns.append(fs)
        columns=','.join(columns)
        sql='create table %s(%s)'%(table_name,columns)

        #调用conn进行sql语句写入数据库
        tooldb=Tooldb()
        tooldb.conn.execute(sql)


class OrangedbSingle(type):
    instance=None
    def __call__(self, *args, **kwargs):
        if OrangedbSingle.instance==None:
            obj=object.__new__(self)
            obj.__init__(*args, **kwargs)
            OrangedbSingle.instance=obj
        return OrangedbSingle.instance


#创建一个工具类,专门负责,表的增删改查
class Tooldb(metaclass=OrangedbSingle):
    #创建工具对象时,就自动创建连接
    def __init__(self):
        self.conn=Connection()
        print('创建一个sql工具')

    #将用户输入信息插入到数据库中
    def save(self,obj):
        columns=[]#字段名
        values=[]#字段值

        for k,v in obj.__dict__.items():
            columns.append(k)
            values.append(v)

        columns=','.join(columns)

        fmt=['%s'for i in values]
        fmt=','.join(fmt)

        sql='insert into %s(%s) values(%s)'%\
            (obj.__class__.__name__,columns,fmt)
        res=self.conn.execute(sql,values)
        return res

    #删除数据库表中的某一行
    def delete(self, obj):
        table_name=obj.__class__.__name__
        sql='delete from %s where %s =%s'%(table_name,obj.__class__.pri_key,obj.id)
        res=self.conn.execute(sql)
        return res

    #更新数据库表中的信息
    def update(self,obj):
        #拼接字符串
        "name = %s,size=%s,author=%s"
        cs=[]#需要修改的字段名
        vs=[]#需要修改的值

        for k,v in obj.__dict__.items():
            c='%s='%k
            c+='%s'
            cs.append(c)
            vs.append(v)
        cs=','.join(cs)

        sql='update %s set %s where id=%s'%\
            (obj.__class__.__name__,cs,obj.id)
        res=self.conn.execute(sql,tuple(vs))
        return res

    #获取数据库表中的信息
    def get(self,cls,id):
        sql='select *from %s where %s=%s'%(cls.__name__,cls.pri_key,id)
        res=self.conn.select(sql)
        if not res:
            return
        obj=object.__new__(cls)
        for k,v in res[0].items():
            if isinstance(v, datetime):
                v = str(v)
            obj.__dict__[k]=v
        return obj

    # 输入形式condition=None>>>di=2,limit=None>>>(0,2)
    def select_many(self,cls,condition=None,args=None,limit=None):
        table_name=cls.__name__
        sql='select *from %s'%table_name
        if condition:
            sql+=' where %s'%condition
        if limit:
            sql+=' limit %s,%s'%(limit[0],limit[1])

        res=self.conn.select(sql,args)

        if not res:
            return
        objs=[]
        for dic in res:
            obj=object.__new__(cls)
            for k,v in dic.items():
                if isinstance(v,datetime):
                    v=str(v)
                obj.__dict__[k]=v
            objs.append(obj)

        return objs


 #处理数据库连接
class Connection:
    #创建连接
    host = '127.0.0.1'
    user = 'root'
    password = '123'
    database = 'ormtest'
    charset = 'utf8'
    autocommit = True  #自动提交sql语句
    current_connect_count=0
    def create_conn(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset,
            autocommit=True  #
        )

    def __init__(self,max_connect=10,retry_time=0.2):
        self.pool=[]
        self.retry_time=retry_time
        self.max_connect=max_connect
        #数据库连接池
        try:
            #开始5个数据库连接
            for i in range(5):
                conn=self.create_conn()
                self.current_connect_count += 1
                #把连接放入列表容器
                self.pool.append(conn)
                print('连接数据库成功')
        except Exception as e:
            print('连接失败',e)

    #创建一个数据库连接池,增删改接口
    def execute(self,sql,args=None,is_select=False):
        while True:
            if not self.pool:
                if self.current_connect_count<self.max_connect:
                    #创建新连接,放到池子中
                    conn=self.create_conn()
                    self.current_connect_count+=1
                    self.pool.append(conn)
                else:
                    time.sleep(self.retry_time)
            else:
                break
        #取出一个连接
        conn=self.pool.pop()
        affect_row=0
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        try:
            affect_row=cursor.execute(sql,args)
        except Exception as e:
            print(e)

        #查询结束,把连接放回pool中
        self.pool.append(conn)
        if is_select:
            return cursor.fetchall()
        return affect_row

    #查询接口
    def select(self,sql,args=None):
        return self.execute(sql,args,is_select=True)