from flask import render_template, url_for
from app import app
import requests

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
    return render_template('dashboard.html')

@app.route('/budgets')
def budgets():
    return render_template('budgets.html')