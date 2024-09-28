from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.services.auth import authenticate_user
from src.services.session import initialize_user_session

doctor_blueprint = Blueprint('doctor_blueprint', __name__)


@doctor_blueprint.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = authenticate_user(email, password, 'doctor')
        if user:
            initialize_user_session(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('doctor_login.html')
