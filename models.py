from flask_login import UserMixin
from extensions import mysql

class User(UserMixin):
    def __init__(self, id, username, name, password, is_admin):
        self.id = id
        self.username = username
        self.name = name  # 사용자 실명 추가
        self.password = password
        self.is_admin = is_admin

def get_user_by_username(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, name, password, user_type FROM login_users WHERE username = %s", (username,))
    data = cursor.fetchone()
    cursor.close()
    if data:
        is_admin = (data[4] == 'teacher')
        return User(data[0], data[1], data[2], data[3], is_admin)
    return None

def get_user_by_id(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, name, password, user_type FROM login_users WHERE id = %s", (user_id,))
    data = cursor.fetchone()
    cursor.close()
    if data:
        is_admin = (data[4] == 'teacher')
        return User(data[0], data[1], data[2], data[3], is_admin)
    return None

def create_user(username, name, password, phone, email, user_type, affiliation, position, agree_terms):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO login_users (username, name, password, phone, email, user_type, affiliation, position, agree_terms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                   (username, name, password, phone, email, user_type, affiliation, position, agree_terms))
    mysql.connection.commit()
    cursor.close()
