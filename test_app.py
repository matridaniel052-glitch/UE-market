from app import create_app

app = create_app()

with app.app_context():
    print("✅ App works!")
    print(f"✅ Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"✅ Secret key set: {bool(app.config['SECRET_KEY'])}")