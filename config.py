from dotenv import load_dotenv
import os

# load .env
load_dotenv()
user = os.environ.get('mysql_id')
pw = os.environ.get('mysql_pw')

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = user
    MYSQL_PASSWORD = pw
    MYSQL_DB = 'login'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
