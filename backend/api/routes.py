"""All routes for the application are declared here"""
from flask_restful import Api
from api import api, app_views
from api.resources.user_resources import Default, UserRegistration, UserLogin, UserLogout, AllUsers, Users
from api.resources.budget_resources import AllUserBudgets

api = Api(app_views)

api.add_resource(Default, '/', strict_slashes=False)
api.add_resource(UserRegistration, '/register', endpoint = 'register', strict_slashes=False)
api.add_resource(UserLogin, '/login', endpoint = 'login', strict_slashes=False)
api.add_resource(UserLogout, '/logout', endpoint = 'logout', strict_slashes=False)
api.add_resource(AllUsers, '/users', endpoint = 'all_users', strict_slashes=False)
api.add_resource(Users, '/users/<int:id>', endpoint = 'users', strict_slashes=False)

api.add_resource(AllUserBudgets, '/users/<int:id>/budgets', endpoint = 'budgets', strict_slashes=False)
