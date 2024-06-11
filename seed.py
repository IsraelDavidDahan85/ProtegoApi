from faker import Faker
from app import app
from models.userModel import UserModel
from database.config import db

fake = Faker()
with app.app_context():
    print("Starting seed...")
    # UserModel.query.delete()
    new_users = []
    for _ in range(20):
        username = fake.user_name()
        email = fake.email()
        new_user = UserModel(name=username, email=email, password="password")
        new_users.append(new_user)
    db.session.add_all(new_users)
    db.session.commit()
    print("Successfully seeded")
