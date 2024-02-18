"""User resources"""
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

class Dashboard(Resource):
    """Handles auth route for dashboard"""
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify({'current_user': current_user})
    