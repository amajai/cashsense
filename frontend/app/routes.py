from flask import render_template, url_for, \
    request, redirect, make_response, flash, session
from app import app
import requests
import os
from requests.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = "{}".format(os.getenv('BACKEND_URL'))
s = requests.Session() # manage server-side cookies


@app.route('/')
def home():
    """Homepage of app"""
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page of app"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            data_login = {'email': email, 'password': password}
            response = s.post(f'{BACKEND_URL}/login', json=data_login)
            data = response.json()
            if response.status_code == 200:
                session['logged_in'] = True
                s.cookies.set('token', data['access_token'])
                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('token', data['access_token'])
                return response
            else:
                flash(response.json().get('message'), 'danger')
                return redirect(url_for('login'))
        except RequestException as e:
            flash(str(e), 'danger')
            return redirect(url_for('login'))
    else:
        if session.get('logged_in', None):
            return redirect(url_for('dashboard'))
        url = url_for('signup')
        name = 'Sign Up'
        return render_template('login.html', link_url=url, link_name=name)


@app.route('/logout', methods=['GET'])
def logout():
    """Logout page of app"""
    response = s.post(f'{BACKEND_URL}/logout')
    if response.status_code == 200:
        session['logged_in'] = False
        s.cookies.clear_session_cookies()
        response = make_response(redirect(url_for('home')))
        response.delete_cookie('token')
        return response
    else:
        flash("You are already logged out!", 'warning')
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Password do not match", 'danger')
            return redirect(url_for('signup'))

        signup_data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password1
        }
        try:
            response = s.post(f'{BACKEND_URL}/register', json=signup_data)
            data = response.json()
            if response.status_code == 201:
                msg = f"({firstname} {lastname} - {email}) {data['message']}"
                flash(msg, 'success')
                return redirect(url_for('login'))
            else:
                flash(response.json().get('message'), 'warning')
                return redirect(url_for('signup'))
        except RequestException as e:
            flash(str(e), 'danger')
            return redirect(url_for('signup'))
    else:
        if session.get('logged_in', None):
            return redirect(url_for('dashboard'))
        url = url_for('login')
        name = 'Login'
        return render_template('signup.html', link_url=url, link_name=name)


@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BACKEND_URL}/dashboard', headers=headers)
    if response.status_code == 200:
        title = 'Dashboard'
        return render_template('dashboard.html', title=title)
    else:
        return response.json(), 401


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
