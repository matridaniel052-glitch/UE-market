from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='fatawudaniel930@gmail.com').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("✅ Success! You are now Admin!")
    else:
        print("❌ User not found. Please register first.")