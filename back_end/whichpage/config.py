#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import redis
import os

# 设置数据库的参数
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '106.52.194.66'
PORT = 3306
DATABASE = 'whichpage'


# 配置信息
class Config(object):

    DEBUG = True
    SECRET_KEY = os.urandom(24)

    # 数据库
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=UTF8MB4'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
