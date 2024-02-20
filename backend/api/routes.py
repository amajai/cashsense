"""All routes for the application are declared here"""
from flask_restful import Api
from api import api, app_views
from api.resources.user_resources import Default, UserRegistration, UserLogin, UserLogout, AllUsers, Users
from api.resources.budget_resources import AllUserBudgets, Budgets
from api.resources.expense_resources import AllBudgetsAndCorrespondingExpenses, AllBudgetExpenses, Expenses


api = Api(app_views)

api.add_resource(Default, '/', strict_slashes=False)
api.add_resource(UserRegistration, '/register', endpoint = 'register', strict_slashes=False)
api.add_resource(UserLogin, '/login', endpoint = 'login', strict_slashes=False)
api.add_resource(UserLogout, '/logout', endpoint = 'logout', strict_slashes=False)
api.add_resource(AllUsers, '/users', endpoint = 'all_users', strict_slashes=False)
api.add_resource(Users, '/users/<int:id>', endpoint = 'users', strict_slashes=False)

api.add_resource(AllUserBudgets, '/users/<int:id>/budgets', endpoint = 'budgets', strict_slashes=False)
api.add_resource(Budgets, '/users/<int:id>/budgets/<int:budget_id>', endpoint = 'budget', strict_slashes=False)

api.add_resource(AllBudgetsAndCorrespondingExpenses, '/users/<int:id>/budgets-expenses', endpoint = 'budgets-expenses', strict_slashes=False)
api.add_resource(AllBudgetExpenses, '/users/<int:id>/budgets/<int:budget_id>/expenses', endpoint = 'expenses', strict_slashes=False)
api.add_resource(Expenses, '/users/<int:id>/budgets/<int:budget_id>/expenses/<int:expense_id>', endpoint = 'expense', strict_slashes=False)
api.add_resource(Dashboard, '/dashboard', strict_slashes=False)
