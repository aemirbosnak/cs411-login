import os


class Config:
    MONGO_URI = 'mongodb://localhost:27017/mydb'
    SECRET_KEY = os.urandom(24)