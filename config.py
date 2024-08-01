import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'mysql 사용자 이름'     # 본인 mysql id 입력
    MYSQL_PASSWORD = 'mysql password' # 본인 mysql pw 입력
    MYSQL_DB = 'login'
