from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.services.auth import authenticate_user
from src.services.session import initialize_user_session

admin_blueprint = Blueprint('admin_blueprint', __name__)


@admin_blueprint.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = authenticate_user(email, password, 'admin')
        if user:
            initialize_user_session(user)
            return redirect(url_for('dashboard'))
        # TODO: use something other than flash to show errors to user
        flash('Invalid credentials')
    return render_template('admin_login.html')
