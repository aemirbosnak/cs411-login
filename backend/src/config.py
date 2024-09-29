import os


class Config:
    MONGO_URI = 'mongodb://localhost:27017/mydb'
    SECRET_KEY = os.urandom(24)

    # JWT settings
    JWT_EXPIRATION_DELTA = 3600  # Token expiration time in seconds (1 hour)
    JWT_SECRET_KEY = 'FUiGgslHZh8sEl5qDD2VJfmWpqdVUyPjZw8e9Je7CQ15bH8HX2lzezUtph6dMxwid3nn+tXMZaX+k7Q'
