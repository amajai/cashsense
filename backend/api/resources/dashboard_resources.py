"""User resources"""
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_user, current_user, logout_user, login_required

from flask import jsonify

class Dashboard(Resource):
    """Handles auth route for dashboard"""
    @jwt_required()
    def get(self):
        if current_user.is_authenticated:
            user = get_jwt_identity()
            return jsonify({'current_user': user})
        else:
            response = jsonify({'error': 'Unauthorized'})
            response.status_code = 401
            return response
