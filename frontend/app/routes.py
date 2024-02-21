from flask import render_template, url_for, \
    request, redirect, make_response, flash, session
from app import app
import requests
import os
from requests.exceptions import RequestException
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
BACKEND_URL = "{}".format(os.getenv('BACKEND_URL'))
s = requests.Session() # manage server-side cookies

def daytime_countdown(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        if end_date < start_date:
            return None

        time_difference = end_date - start_date
        days = time_difference.days
        countdown_str = f"{days} days"
        return countdown_str
    except Exception as e:
        return e

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
                session['current_user'] = data.get('data') 
                response = make_response(redirect(url_for('dashboard')))
                return response
            else:
                flash(response.json().get('message'), 'danger')
                return redirect(url_for('login'))
        except RequestException as e:
            flash(str(e), 'danger')
            return redirect(url_for('login'))
    else:
        if 'current_user' in session:
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
        session.pop('current_user', None)
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
        if 'current_user' in session:
                return redirect(url_for('dashboard'))
        url = url_for('login')
        name = 'Login'
        return render_template('signup.html', link_url=url, link_name=name)


@app.route('/dashboard')
def dashboard():
    id = session['current_user']['id']
    response = s.get(f'{BACKEND_URL}')
    if response.status_code == 200:
        res = s.get(f'{BACKEND_URL}/users/{id}/budgets-expenses')
        if res.json().get('data'):
            data = {}
            budget_expenses = res.json().get('data')
            overall_budget = 0
            overall_expense = 0
            budget_count = 0
            expense_count = 0
            budgets = []
            for pairs in budget_expenses:
                budget_count += 1
                overall_budget += pairs['budget']['amount']
                budget = pairs['budget']
                if pairs['expenses']:
                    current_total_expense = 0
                    for expense in pairs['expenses']:
                        expense_count += 1
                        current_total_expense += expense['amount']
                    budget['total_expense'] = current_total_expense
                    overall_expense += current_total_expense
                else:

                    budget['total_expense'] = 0
                budget['remaining_days'] = daytime_countdown(pairs['budget']['start_date'], pairs['budget']['end_date'])
                budgets.append(budget)
            data['overall_budget'] = overall_budget
            data['overall_expense'] = overall_expense
            data['budget_count'] = budget_count
            data['expense_count'] = expense_count
            data['budgets'] = budgets
        else:
            data = {
                'overall_budget': 0,
                'overall_expense': 0,
                'budget_count': 0,
                'expense_count': 0,
                'budgets': []
            }
        title = 'Dashboard'
        return render_template('dashboard.html', title=title, data=data)
    else:
        response = make_response(redirect(url_for('login')))
        session.pop('current_user', None)
        return response


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
    if request.method == 'POST':
        response = s.delete(f'{BACKEND_URL}/users/{id}')
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('users'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('users'))
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}')
        if response.status_code == 200:
            title = 'Delete User'
            user = response.json().get('data')
            return render_template('user_delete.html', title=title, user=user)
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('users'))


@app.route('/dashboard/budgets', methods=['GET'])
def budgets():
    id = session['current_user']['id']
    title = 'Budgets'
    response = s.get(f'{BACKEND_URL}/users/{id}/budgets')
    if response.status_code == 200:
        budgets = response.json().get('data')
        sorted_budgets = sorted(budgets, key=lambda d: d['id'], reverse=True)
        return render_template('budgets.html', title=title, budgets=sorted_budgets)
    elif response.status_code == 404:
        budgets = []
        return render_template('budgets.html', title=title, budgets=budgets)
    else:
        flash(response.json().get('message'), 'danger')
        return redirect(url_for('dashboard'))


@app.route('/dashboard/budgets/add', methods=['GET', 'POST'])
def add_budget():
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    title = 'Add Budget'
    id = session['current_user']['id']
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        start_date_datefrmt = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_datefrmt = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date_datefrmt >= end_date_datefrmt:
            flash("Start Date cannot be greater than End Date", 'warning')
            return redirect(request.url)

        data_budget = {
            'name': name,
            'amount': amount,
            'start_date': start_date_datefrmt.strftime('%d/%m/%Y'),
            'end_date': end_date_datefrmt.strftime('%d/%m/%Y'),
        }

        response = s.post(f'{BACKEND_URL}/users/{id}/budgets', json=data_budget)
        if response.status_code == 201:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('budgets'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}/budgets')
        if response.status_code == 200:
            budgets = response.json().get('data')
            return render_template('budget_add.html', title=title, budgets=budgets)
        elif response.status_code == 404:
            budgets = []
            return render_template('budget_add.html', title=title, budgets=budgets)
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)


@app.route('/dashboard/budgets/<int:budget_id>', methods=['GET', 'POST'])
def edit_budget(budget_id):
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login'))
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    id = session['current_user']['id']
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        start_date_datefrmt = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_datefrmt = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date_datefrmt >= end_date_datefrmt:
            flash("Start Date cannot be greater than End Date", 'warning')
            return redirect(request.url)

        data_budget = {
            'name': name,
            'amount': amount,
            'start_date': start_date_datefrmt.strftime('%d/%m/%Y'),
            'end_date': end_date_datefrmt.strftime('%d/%m/%Y'),
        }
        response = s.put(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}', json=data_budget)
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('budgets'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}')
        if response.status_code == 200:
            title = 'Edit Budget'
            budget = response.json().get('data')
            return render_template('budget_edit.html', title=title, budget=budget)
        elif response.status_code == 401:
            return redirect(url_for('dashboard'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)


@app.route('/dashboard/budgets/<int:budget_id>/delete', methods=['GET', 'POST'])
def delete_budget(budget_id):
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    id = session['current_user']['id']
    if request.method == 'POST':
        response = s.delete(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}')
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('budgets'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('budgets'))
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}')
        if response.status_code == 200:
            title = 'Delete Budget'
            budget = response.json().get('data')
            return render_template('budget_delete.html', title=title, budget=budget)
        elif response.status_code == 401:
            return redirect(url_for('dashboard'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('budgets'))


@app.route('/dashboard/expenses', methods=['GET'])
def expenses():
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    id = session['current_user']['id']
    res = s.get(f'{BACKEND_URL}/users/{id}/budgets-expenses')

    if not res.json().get('data'):
        flash(f"{res.json().get('message')}. Please add a budget to use expenses", 'warning')
        return redirect(url_for('add_budget'))
    
    budget_totals = {}
    if res.status_code == 200:
        data = res.json().get('data')
        for pairs in data:
            if pairs['expenses']:
                total = 0
                for expense in pairs['expenses']:
                    total += float(expense['amount'])
                budget_totals[pairs['budget']['id']] = total
            else:
                budget_totals[pairs['budget']['id']] = 0
        title = 'Expenses'
        return render_template('expenses.html', title=title, data=data)
    elif res.status_code == 401:
        return redirect(url_for('dashboard'))
    else:
        flash(res.json().get('message'), 'danger')
        return redirect(request.url)


@app.route('/dashboard/expenses/add', methods=['GET', 'POST'])
def expense_add():
    id = session['current_user']['id']
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        budget_id = request.form.get('budget-select')
        data_expense = {
            'category': category,
            'amount': amount,
        }
        response = s.post(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}/expenses', json=data_expense)
        if response.status_code == 201:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('expenses'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}/budgets')
        if response.status_code == 200:
            title = 'Add Expense'
            budgets = response.json().get('data')
            return render_template('expense_add.html', title=title, budgets=budgets)
        elif response.status_code == 404:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('expenses'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('dashboard'))


@app.route('/dashboard/budget/<int:budget_id>/expenses/<int:expense_id>', methods=['GET', 'POST'])
def expense_edit(budget_id, expense_id):
    id = session['current_user']['id']
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        data_expense = {
            'category': category,
            'amount': amount,
        }

        response = s.put(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}/expenses/{expense_id}', json=data_expense)
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('expenses'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}/expenses/{expense_id}')
        if response.status_code == 200:
            title = 'Edit Expense'
            expense = response.json().get('data')
            budgets = s.get(f'{BACKEND_URL}/users/{id}/budgets').json().get('data')
            return render_template('expense_edit.html', title=title, expense=expense, budgets=budgets)
        elif response.status_code == 401:
            return redirect(url_for('expenses'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(request.url)


@app.route('/dashboard/budget/<int:budget_id>/expenses/<int:expense_id>/delete', methods=['GET', 'POST'])
def expense_delete(budget_id, expense_id):
    id = session['current_user']['id']
    response = s.get(f'{BACKEND_URL}')
    if response.status_code != 200:
        return redirect(url_for('login')) 
    if request.method == 'POST':
        response = s.delete(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}/expenses/{expense_id}')
        if response.status_code == 200:
            flash(response.json().get('message'), 'success')
            return redirect(url_for('expenses'))
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('expenses'))
    else:
        response = s.get(f'{BACKEND_URL}/users/{id}/budgets/{budget_id}/expenses/{expense_id}')
        if response.status_code == 200:
            title = 'Delete Expense'
            expense = response.json().get('data')
            return render_template('expense_delete.html', title=title, expense=expense)
        else:
            flash(response.json().get('message'), 'danger')
            return redirect(url_for('expenses'))