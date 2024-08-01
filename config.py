import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
<<<<<<< HEAD
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'newisql@5506'
=======
    MYSQL_USER = 'mysql 사용자 이름'
    MYSQL_PASSWORD = 'mysql password'
>>>>>>> d0bdff1 (window에서 구동 가능하게 수정)
    MYSQL_DB = 'login'
