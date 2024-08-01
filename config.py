import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'mysql 사용자 이름'
    MYSQL_PASSWORD = 'mysql password'
    MYSQL_DB = 'login'
