from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ue-market-secret-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopgh.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'static', 'images'
    )
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes.auth import auth
    from .routes.shop import shop
    from .routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(shop)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app