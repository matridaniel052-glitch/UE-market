from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    image = db.Column(db.String(300), default='default.jpg')
    category = db.Column(db.String(100))
    market = db.Column(db.String(100), default='Bolga')
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.Float)
    status = db.Column(db.String(50), default='pending')
    date = db.Column(db.DateTime, default=datetime.utcnow)