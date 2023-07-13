from flask import Blueprint, render_template, Response, request, flash
import cv2

auth = Blueprint('auth', __name__)
    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolen=True)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if len(email) < 4:
            flash('Email must be greater then 4 character', category='error')
        elif len(name) < 2:
            flash('Name must be greater then 2', category='error')
        elif len(password) < 4:
            flash('Password must be greater then 4 character', category='error')
        else:
            flash('success', category='success')
    return render_template("sign_up.html")