# -*- codeing = utf-8 -*-
# @Time : 2024/1/6 15:42
# @Author : dujinjie
# @File : login.py
# @Software : PyCharm

import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456', db='db_user', charset='utf8')
cur = conn.cursor()


def is_null(username, password):
    if (username == '' or password == ''):
        return True
    else:
        return False


def close(conn, cur):
    if cur:
        cur.close
    if conn:
        conn.close


def is_existed(username, password):
    sql = "SELECT * FROM tb_user WHERE username ='" + username + "' and password ='" + password + "'"
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    if (len(result) == 0):
        return False
    else:
        return True


def exist_user(username):
    sql = "SELECT * FROM tb_user WHERE username ='" + username + "'"
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    if (len(result) == 0):
        return False
    else:
        return True