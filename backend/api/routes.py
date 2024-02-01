"""All routes for the application are declared here"""
from flask_restful import Api
from api import api, app_views
from api.resources.user_resources import Default, UserRegistration, UserLogin, UserLogout

api = Api(app_views)

api.add_resource(Default, '/', strict_slashes=False)
api.add_resource(UserRegistration, '/register', endpoint = 'user', strict_slashes=False)
api.add_resource(UserLogin, '/login', strict_slashes=False)
api.add_resource(UserLogout, '/logout', strict_slashes=False)
