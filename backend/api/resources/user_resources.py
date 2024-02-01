"""User resources"""
from flask_restful import Resource, reqparse
from api.models.user_models import User
from api import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


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
            return {'message': 'An error occured, ensure you are using the right datatypes and your request body is properly formatted'}
        

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
            return {'message': 'User with email - {} is not registered'.format(data['email'])}

        if bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            return {'message': 'Login successful'}
        else:
            return {'message': 'Invalid credentials'}
        

class UserLogout(Resource):
    """/logout route handler"""
    @login_required
    def get(self):
        logout_user()
        return {'message': 'Logged out Successfully'}
