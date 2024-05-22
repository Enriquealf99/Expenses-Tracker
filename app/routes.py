from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import extract, func
from app import db
from app.models import User, Expense, Category
from app.forms import EditExpenseForm, RegistrationForm, LoginForm, ExpenseForm
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.asc()).all()
    return render_template('dashboard.html', expenses=expenses)

@bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            category_id=form.category.data,
            date=form.date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_expense.html', form=form)

@bp.route('/list_categories')
@login_required
def list_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('list_categories.html', categories=categories)


@bp.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = EditExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.category_id = form.category.data
        expense.date = form.date.data
        expense.description = form.description.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('edit_expense.html', form=form, expense=expense)

@bp.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))



@bp.route('/reports/monthly')
@login_required
def monthly_report():
    current_year = datetime.now().year
    expenses = Expense.query.filter_by(user_id=current_user.id).filter(extract('year', Expense.date) == current_year).order_by(Expense.date).all()
    monthly_expenses = db.session.query(
        extract('month', Expense.date).label('month'),
        func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).filter(extract('year', Expense.date) == current_year).group_by('month').all()
    return render_template('monthly_report.html', expenses=expenses, monthly_expenses=monthly_expenses)

@bp.route('/reports/yearly')
@login_required
def yearly_report():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date).all()
    yearly_expenses = db.session.query(
        extract('year', Expense.date).label('year'),
        func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by('year').all()
    return render_template('yearly_report.html', expenses=expenses, yearly_expenses=yearly_expenses)



