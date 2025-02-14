# -*- codeing = utf-8 -*-
# @Time : 2024/1/6 15:42
# @Author : dujinjie
# @File : register.py
# @Software : PyCharm

import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', db='db_user', charset='utf8')
cur = conn.cursor()


def add_user(username, password):
    # sql commands
    sql = "INSERT INTO tb_user(username, password) VALUES ('" + username + "','" + password + "')"
    conn.ping(reconnect=True)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.cursor()
    conn.close()