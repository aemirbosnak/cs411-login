import os
from flask import Flask, render_template, redirect, url_for, session
from src.config import Config
from src.extensions import mongo
from src.routes.admin import admin_blueprint
from src.routes.doctor import doctor_blueprint

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.config.from_object(Config)
app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

# Init MongoDB
mongo.init_app(app)

# Register blueprints
app.register_blueprint(admin_blueprint)
app.register_blueprint(doctor_blueprint)

""" MIDDLEWARE FUNCTIONS """


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


""" ROUTING FUNCTIONS"""


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


# Common Dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' in session and 'role' in session:
        return render_template('dashboard.html',
                               firstName=session['firstName'],
                               lastName=session['lastName'],
                               role=session['role'])
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    session.pop('email', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
