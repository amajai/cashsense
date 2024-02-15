from flask import render_template, url_for, Flask, session, request
from app import app
import requests
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    link_url = url_for('signup')
    link_name = 'Sign Up'
    return render_template('login.html', link_url=link_url, link_name=link_name)

@app.route('/signup')
def signup():
    link_url = url_for('login')
    link_name = 'Login'
    return render_template('signup.html', link_url=link_url, link_name=link_name)

@app.route('/dashboard')
def dashboard():
    title = 'Dashboard'
    return render_template('dashboard.html', title=title)

@app.route('/budgets')
def budgets():
    title = 'Budgets'
    return render_template('budgets.html', title=title)

@app.route('/transactions')
def transactions():
    title = 'Transactions'
    return render_template('transactions.html', title=title)

@app.route('/expense')
def expense():
    title = 'Expense'
    return render_template('expense.html', title=title)
