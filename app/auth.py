from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils import is_valid_email
from werkzeug.security import generate_password_hash
from models import User
from database import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        name = request.form.get('full_name','').strip()
        password = request.form.get('password','')
        confirm_password = request.form.get('confirm_password','')
        print( email, name, password, confirm_password)

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
        

        



        


    
            
        
   
        # Here you would typically add logic to create the user
        # and store it in the database
    return render_template('sign-up.html')