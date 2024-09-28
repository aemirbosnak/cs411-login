from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.services.auth import login_user

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = login_user(email, password, 'admin')
        if user:
            session['email'] = user['email']
            session['role'] = user['role']
            session['firstName'] = user['firstName']
            session['lastName'] = user['lastName']
            return redirect(url_for('dashboard'))
        # TODO: use something other than flash to show errors to user
        flash('Invalid credentials')
    return render_template('admin_login.html')
