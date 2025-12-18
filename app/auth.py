from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils import is_valid_email
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
from flask_login import login_user, logout_user
from routes import bp

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        name = request.form.get('full_name','').strip()
        password = request.form.get('password','')
        confirm_password = request.form.get('confirm_password','')

        existing_email = User.query.filter_by(email=email).first()

        if not name or not password or not email or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for('auth.sign_up'))
        if not is_valid_email(email):
            flash("Invalid email address", "error")
            return redirect(url_for('auth.sign_up'))
        if existing_email:
            flash("Email already registered", "error")
            return redirect(url_for('auth.sign_up'))
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('auth.sign_up'))
        if len(password) < 8:
            flash("Password must be at least 8 characters long", "error")
            return redirect(url_for('auth.sign_up'))
        
        new_user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template('sign-up.html')
    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials, try again", "error")
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        flash("Logged in successfully!", "success")
        return redirect(url_for('bp.incidents'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    flash("Logged out ", "Logged out")
    return redirect(url_for('auth.login'))
