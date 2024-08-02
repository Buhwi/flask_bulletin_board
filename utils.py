from flask import current_app, g, redirect, url_for
from flask_login import current_user  # 여기에 current_user 추가
from models import User
import pymysql
from werkzeug.utils import secure_filename
import os

def id_one_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return redirect(url_for('routes.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def get_user_by_username(username):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT id, username, name, password, user_type FROM login_users WHERE username = %s", (username,))
        data = cursor.fetchone()
    if data:
        is_admin = (data['user_type'] == 'teacher')
        return User(data['id'], data['username'], data['name'], data['password'], is_admin)
    return None

def get_user_by_id(user_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT id, username, name, password, user_type FROM login_users WHERE id = %s", (user_id,))
        data = cursor.fetchone()
    if data:
        is_admin = (data['user_type'] == 'teacher')
        return User(data['id'], data['username'], data['name'], data['password'], is_admin)
    return None

def create_user(username, name, password, phone, email, user_type, affiliation, position, agree_terms):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO login_users (username, name, password, phone, email, user_type, affiliation, position, agree_terms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                       (username, name, password, phone, email, user_type, affiliation, position, agree_terms))
        db.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure the upload folder exists
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        try:
            file.save(file_path)
            print(f"File saved to {file_path}")
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    return None
