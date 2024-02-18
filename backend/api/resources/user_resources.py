"""User resources"""
from flask_restful import Resource, reqparse, fields, marshal
from api.models.user_models import User
from api import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required

from flask import jsonify
from api import app
from datetime import datetime, timedelta, timezone
import json

user_fields = {
    'id': fields.Integer,
    'rank': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'password': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}


class Default(Resource):
    """Api home route handler (/)"""
    def get(self):
        """GET / """
        return {"message": "Welcome to CashSense API"}

class UserRegistration(Resource):
    """/register route handler"""
    def post(self):
        """POST /register """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('firstname', help='This field is required', type = str, location = 'json', required=True)
            parser.add_argument('lastname', help='This field is required', type = str, location = 'json', required=True)
            parser.add_argument('email', help='This field is required', type = str, location = 'json', required=True)
            parser.add_argument('password', help='This field is required', type = str, location = 'json', required=True)
            data = parser.parse_args()

            if User.query.filter_by(email=data['email']).first():
                return {'message': 'User with email - {} already exists, try another email'.format(data['email'])}
            
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            new_user = User(
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'],
                password=data['password']
            )

            db.session.add(new_user)
            db.session.commit()

            return {'message': 'User registered successfully', 'data': data }, 201
        except Exception as err:
            return {'message': 'An error occured, ensure you are using the right keys, datatypes and your request body is properly formatted'}, 400
        
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response

class UserLogin(Resource):
    """/login route handler"""
    def post(self):
        """POST /login"""
        parser = reqparse.RequestParser()
        parser.add_argument('email', help='This field is required', type = str, location = 'json', required=True)
        parser.add_argument('password', help='This field field is required', type = str, location = 'json', required=True)
        data = parser.parse_args()

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {'message': 'User with email - {} is not registered'.format(data['email'])}, 400

        if bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            user = marshal(user, user_fields)
            access_token = create_access_token(identity=data['email'])
            return {'message': 'Login successful', 'data': user, "access_token":access_token}
        else:
            return {'message': 'Invalid credentials'}, 400
        

class UserLogout(Resource):
    """/logout route handler"""
    @login_required
    def post(self):
        logout_user()
        res = jsonify({'message': 'Logged out Successfully'})
        unset_jwt_cookies(res)
        return res
    

class AllUsers(Resource):
    """/users route handler"""
    @login_required
    def get(self):
        """GET /users """
        try:
            if current_user.rank == 1:
                user = User.query.all()
                if user:
                    # Use marshal to serialize the user object
                    user = marshal(user, user_fields)
                    return {'message': 'Successful', 'data': user}
                else:
                    return {'message': 'Users not found'}, 404
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        

class Users(Resource):
    """/users/<int:id> route handler"""
    @login_required
    def get(self, id):
        """GET /users/<int:id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                user = User.query.get(id)
                if user:
                    # Use marshal to serialize the user object
                    user = marshal(user, user_fields)
                    return {'message': 'Successful', 'data': user}
                else:
                    return {'message': 'User not found'}, 404
            else:
                return {'message': "You are trying to access another user's detail"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        
    @login_required
    def put(self, id):
        """ PUT /users/<int:id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                parser = reqparse.RequestParser()
                parser.add_argument('firstname', type=str, location='json')
                parser.add_argument('lastname', type=str, location='json')
                parser.add_argument('email', type=str, location='json')
                parser.add_argument('password', type=str, location='json')
                data = parser.parse_args()

                user = User.query.get(id)
                if not user:
                    return {'message': 'User not found'}, 404

                # Update user attributes if the fields are provided in the request
                if data['firstname']:
                    user.firstname = data['firstname']
                if data['lastname']:
                    user.lastname = data['lastname']
                if data['email']:
                    # Check if the new email is not already taken
                    existing_user = User.query.filter_by(email=data['email']).first()
                    if existing_user and existing_user.id != id:
                        return {'message': 'Email is already in use by another user'}, 400
                    user.email = data['email']
                if data['password']:
                    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

                db.session.commit()

                return {'message': 'User updated successfully', 'data': {k: v for k, v in data.items() if v is not None}}

            else:
                return {'message': "You are not authorized to update this user's details"}, 403
        except Exception as err:
            return {'message': str(err)}, 500
        
    @login_required
    def delete(self, id):
        """DELETE /users/<int:id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                user = User.query.get(id)
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return {'message': 'User Deleted', 'data': {'id': user.id, 'email': user.email}}
                else:
                    return {'message': 'User not found'}, 404
            else:
                return {'message': "You are trying to access another user's detail"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again, ensure your request is correct!'}, 500
