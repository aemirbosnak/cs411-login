import os

from flask import Flask, render_template, request, session, redirect, url_for, flash
from src.models import mongo, find_by_email_role
import bcrypt
from src.config import Config

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.config.from_object(Config)

# Init MongoDB
mongo.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = find_by_email_role(email, 'admin')
        if user and bcrypt.checkpw(password.encode('utf-8', user['password']), user['password'].encode('utf-8')):
            session['email'] = user['email']
            session['role'] = user['role']
            session['firstName'] = user['firstName']
            session['lastName'] = user['lastName']
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html')


# Doctor Login
@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = find_by_email_role(email, 'doctor')
        print(user)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['email'] = user['email']
            session['role'] = user['role']
            session['firstName'] = user['firstName']
            session['lastName'] = user['lastName']
            print("success")
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('doctor_login.html')


# Common Dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' in session and 'role' in session:
        return render_template('dashboard.html',
                               firstName=session['firstName'],
                               lastName=session['lastName'],
                               role=session['role'])
    return redirect(url_for('doctor_login'))


@app.route('/logout')
def logout():
    session.clear()
    session.pop('email', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
