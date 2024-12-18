from flask import Flask, session
from flask_cors import CORS

from config import Config
from modules.auth.routes import auth_bp
from modules.admission.routes import patient_bp
from modules.rooms.routes import room_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(room_bp)


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
    app.run(host='0.0.0.0', port=5000, debug=True)
