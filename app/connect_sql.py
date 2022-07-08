# -*- coding:utf-8 -*-
"""
project: pythonProject1
file: connect_sql
author: Yujin
create date: 2022/6/21 14:59
description: 
"""
import pymysql
class Mysql(object):
    def __init__(self,userId):

        # 连接历史轨迹数据库
        self.DBHOST = 'localhost'
        self.DBUESR = 'root'
        self.DBPASS = 'Cabinda@9527'
        self.DBNAME = 'historic_position'
        self.userId = userId
        try:
            self.db = pymysql.connect(user=self.DBUESR, password=self.DBPASS, host=self.DBHOST,
                                      database=self.DBNAME)  # 用户名，密码，主机名，数据库，端口
            print('数据库连接成功')
        #     # 数据库连接成功之后，1. 声明一个游标
            self.cursor = self.db.cursor()
        # 2. #判断这张表是否存在，若存在，则跳过创建表操作
            sqlQuery = "create table if not exists  t_{} (id int primary key auto_increment, Px float not null, Py float not null)".format(
                userId)
            self.cursor.execute(sqlQuery)
        except pymysql.Error as e:
            print('数据库表格创建失败：' + str(e))

    # 执行插入函数
    def insertdata(self, px, py):
        sql = "insert into t_{0}(Px,Py) values ({1}, {2})".format(self.userId, px, py)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            # 如果发生错误就回滚，建议使用这样发生错误就不会对表数据有影响
            self.db.rollback()
        return

    # 查询数据长度
    def getdatalen(self):
        sql = "select count(*) from t_{}".format(self.userId)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有的记录
        results = self.cursor.fetchall()
        return results[0][0]

    # 删除数据函数
    def deletedata(self):
        sqlQuery = "delete from t_{} where id <= 50".format(self.userId)
        sqlQuery1 = "ALTER TABLE t_{} MODIFY id int NOT NULL FIRST,DROP PRIMARY KEY ".format(self.userId)
        sqlQuery2 = "ALTER TABLE t_{} ADD id1 int Not NULL AUTO_INCREMENT FIRST,ADD PRIMARY KEY (id1) ".format(
            self.userId)
        sqlQuery3 = "ALTER TABLE t_{} DROP id ".format(self.userId)
        sqlQuery4 = "ALTER TABLE t_{} CHANGE id1 id int NOT NULL AUTO_INCREMENT FIRST ".format(self.userId)
        try:
            # 执行sql语句
            self.cursor.execute(sqlQuery)
            self.cursor.execute(sqlQuery1)
            self.cursor.execute(sqlQuery2)
            self.cursor.execute(sqlQuery3)
            self.cursor.execute(sqlQuery4)
            # 提交数据
            self.db.commit()
        except:
            # 如果发生错误就回滚，建议使用这样发生错误就不会对表数据有影响
            self.db.rollback()
        return

    # 查询数据
    def getdata(self):
        sql = "select Px,Py from t_{}".format(self.userId)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有的记录
        results = self.cursor.fetchall()
        return results

        # 查询数据
    def getgapdata(self,start,end):
        sql = "select Px,Py from t_{0} limit {1},{2}".format(self.userId,start,end)
        # 执行sql语句
        self.cursor.execute(sql)
        # 获取所有的记录
        results = self.cursor.fetchall()
        return results


    # # 关闭
    # def __del__(self):
    #     self.db.close()
