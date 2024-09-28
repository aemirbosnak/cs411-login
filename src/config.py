import os


class Config:
    MONGO_URI = 'mongodb://localhost:27017/mydb'
    SECRET_KEY = os.urandom(24)

    # Session settings
    SESSION_COOKIE_HTTPONLY = True  # Prevent JS to access session cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # Prevention from CSRF
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
