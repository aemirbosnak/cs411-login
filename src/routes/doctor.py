from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.services.auth import login_user

doctor_bp = Blueprint('doctor_bp', __name__)


@doctor_bp.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = login_user(email, password, 'doctor')
        # TODO: make session initialization into function to remove duplicated code
        if user:
            session['email'] = user['email']
            session['role'] = user['role']
            session['firstName'] = user['firstName']
            session['lastName'] = user['lastName']
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('doctor_login.html')
