import os
from flask import Flask, session
from src.config import Config
from src.extensions import mongo
from src.routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

# Init MongoDB
mongo.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


if __name__ == '__main__':
    app.run(debug=True)
