from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationship to Expense with a unique backref name
    expenses = db.relationship('Expense', backref='user_expenses', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __table_args__ = {'extend_existing': True}

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Use a unique backref name for the Category-Expense relationship
    expenses = db.relationship('Expense', backref='category_expenses')


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200))

    # Foreign key linking Expense to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Foreign key linking Expense to Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # Relationship to User (now using user_expenses)
    user = db.relationship('User', backref='user_expenses')

    # Relationship to Category (now using category_expenses)
    category = db.relationship('Category', backref='category_expenses')





    

