import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ue-market-secret-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///shopgh.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'app', 'static', 'images'
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024