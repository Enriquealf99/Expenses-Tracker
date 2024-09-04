import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User, Category
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Expense')

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        # Load all categories for the dropdown without filtering by user_id
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]



class EditExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Update Expense')

    def __init__(self, *args, **kwargs):
        super(EditExpenseForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]

class MonthYearForm(FlaskForm):
    current_year = datetime.datetime.now().year
    months = [(i, datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    years = [(i, i) for i in range(current_year - 50, current_year + 1)]

    month = SelectField('Month', choices=months, validators=[DataRequired()])
    year = SelectField('Year', choices=years, validators=[DataRequired()])
    submit = SubmitField('Generate Report')


class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already in use. Please choose a different one.')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

