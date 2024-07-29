from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import get_user_by_username, get_user_by_id, create_user
from utils import id_one_required
from extensions import mysql, login_manager

bp = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phone']
        email = request.form['email']
        user_type = request.form['user_type']
        affiliation = request.form['affiliation']
        position = request.form['position']
        agree_terms = 'agree_terms' in request.form

        create_user(username, name, password, phone, email, user_type, affiliation, position, agree_terms)
        flash('Registration successful! You can now log in.')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, title, content FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    return render_template('index.html', posts=posts)

@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
@id_one_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('routes.index'))
    return render_template('create_post.html')

@bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@id_one_required
def edit_post(post_id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('routes.index'))
    cursor.execute("SELECT id, title, content FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    return render_template('edit_post.html', post=post)

@bp.route('/post/delete/<int:post_id>')
@login_required
@id_one_required
def delete_post(post_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('routes.index'))
