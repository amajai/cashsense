from flask import render_template, url_for, \
    request, redirect, make_response, flash, session
from app import app
import requests
import os
from requests.exceptions import RequestException
from dotenv import load_dotenv
import atexit


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
                session['current_user'] = data.get('data') 
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
        response = make_response(redirect(url_for('home')))
        response.delete_cookie('token') 
        response.set_cookie('session', '', expires=0)
        session.clear()
        s.cookies.clear_session_cookies()
        s.cookies.clear_expired_cookies()
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
    headers = {'Authorization': f'Bearer {token}'}
    response = s.get(f'{BACKEND_URL}/dashboard', headers=headers)
    if response.status_code == 200:
        title = 'Dashboard'
        return render_template('dashboard.html', title=title)
    else:
        response = make_response(redirect(url_for('login')))
        response.delete_cookie('token') 
        response.set_cookie('session', '', expires=0)
        session.clear()
        s.cookies.clear_session_cookies()
        s.cookies.clear_expired_cookies()
        return response


@app.route('/dashboard/budgets')
def budgets():
    title = 'Budgets'
    return render_template('budgets.html', title=title)


@app.route('/dashboard/transactions')
def transactions():
    title = 'Transactions'
    return render_template('transactions.html', title=title)


@app.route('/dashboard/expense')
def expense():
    title = 'Expense'
    return render_template('expense.html', title=title)


@app.route('/dashboard/users', methods=['GET'])
def users():
    response = s.get(f'{BACKEND_URL}/users')
    if response.status_code == 200:
        title = 'All Users'
        users = response.json().get('data')
        sorted_users = sorted(users, key=lambda d: d['id'], reverse=True)
        return render_template('users.html', title=title, users=sorted_users)
    else:
        return redirect(url_for('dashboard'))
    

@app.route('/dashboard/users/<int:id>', methods=['GET', 'POST'])
def user(id):
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        rank = request.form.get('rank', 0)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        data_update = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'rank': int(rank),
        }

        if password1:
            if password1 != password2:
                flash("Password do not match", 'danger')
                return redirect(request.url)
            data_update['password'] = password1

        response = s.put(f'{BACKEND_URL}/users/{id}', json=data_update)
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(request.url)
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('users'))
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}')
        if response.status_code == 200:
            title = 'User - {} {}'.format(session['current_user']['firstname'].title(), session['current_user']['lastname'].title())
            user = response.json().get('data')
            return render_template('user.html', title=title, user=user)
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('users'))
    

@app.route('/dashboard/users/<int:id>/delete', methods=['GET', 'POST'])
def user_delete(id):
    print('r', request.method )
    if request.method == 'POST':
        response = s.delete(f'{BACKEND_URL}/users/{id}')
        print(response.json())
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('users'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('users'))
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}')
        if response.status_code == 200:
            title = 'Delete'
            user = response.json().get('data')
            return render_template('delete.html', title=title, user=user)
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('users'))