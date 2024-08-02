from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from utils import id_one_required, get_user_by_username, get_user_by_id, create_user, save_file
from extensions import login_manager
import os

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
    try:
        db = current_app.get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT id, title FROM posts")
            posts = cursor.fetchall()
    except Exception as e:
        print(f"Database connection failed: {e}")
        return "Database connection failed", 500
    return render_template('index.html', posts=posts)

@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
@id_one_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']
        document_file = request.files['document']
        
        # Save files
        image_filename = save_file(image_file)
        document_filename = save_file(document_file)
        
        # Log filenames to check if they are saved
        print(f"Image Filename: {image_filename}")
        print(f"Document Filename: {document_filename}")
        
        db = current_app.get_db()
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO posts (title, content, image, document) VALUES (%s, %s, %s, %s)", (title, content, image_filename, document_filename))
            db.commit()
        return redirect(url_for('routes.index'))
    return render_template('create_post.html')

@bp.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    db = current_app.get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT id, title, content, image, document FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
    return render_template('view_post.html', post=post)

@bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@id_one_required
def edit_post(post_id):
    db = current_app.get_db()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']
        document_file = request.files['document']
        
        # Save files
        image_filename = save_file(image_file)
        document_filename = save_file(document_file)
        
        # Log filenames to check if they are saved
        print(f"Image Filename: {image_filename}")
        print(f"Document Filename: {document_filename}")
        
        with db.cursor() as cursor:
            cursor.execute("UPDATE posts SET title = %s, content = %s, image = %s, document = %s WHERE id = %s", (title, content, image_filename, document_filename, post_id))
            db.commit()
        return redirect(url_for('routes.index'))
    with db.cursor() as cursor:
        cursor.execute("SELECT id, title, content, image, document FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
    return render_template('edit_post.html', post=post)

@bp.route('/post/delete/<int:post_id>')
@login_required
@id_one_required
def delete_post(post_id):
    db = current_app.get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        db.commit()
    return redirect(url_for('routes.index'))

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
