"""Budget resources"""
from flask_restful import Resource, reqparse, fields, marshal
from datetime import datetime
from api.models.user_models import User
from api.models.budget_models import Budget
from api import db
from flask_login import current_user, login_required

    
budget_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'amount': fields.Integer,
    'start_date': fields.String(attribute=lambda x: x.start_date.strftime('%Y-%m-%d')),
    'end_date': fields.String(attribute=lambda x: x.end_date.strftime('%Y-%m-%d')),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class AllUserBudgets(Resource):
    """/users/id/budgets route handler"""
    @login_required
    def post(self, id):
        """POST /users/id/budgets """
        try:
            if current_user.id == id or current_user.rank == 1:
                parser = reqparse.RequestParser()
                parser.add_argument('name', help='This field is required', type = str, location = 'json', required=True)
                parser.add_argument('amount', help='This field is required', type = int, location = 'json', required=True)
                parser.add_argument('start_date', help='This field is required', type = str, location = 'json', required=True)
                parser.add_argument('end_date', help='This field is required', type = str, location = 'json', required=True)
                data = parser.parse_args()
                
                start_date_str = data['start_date']
                end_date_str = data['end_date']
                start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
                end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
                print(current_user.id)
                print(type(end_date))
                new_budget = Budget(
                    user_id=current_user.id,
                    name=data['name'],
                    amount=data['amount'],
                    start_date=start_date,
                    end_date=end_date
                )

                db.session.add(new_budget)
                db.session.commit()
                return {'message': 'Budget added successfully', 'data': data }, 201
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception:
            return {'message': 'An error occured, ensure you are using the right keys, datatypes and your request body is properly formatted'}, 400


    @login_required
    def get(self, id):
        """GET /users/id/budgets """
        try:
            if current_user.id == id or current_user.rank == 1:
                budgets = Budget.query.filter_by(user_id=id).all()
                print(budgets)
                if budgets:
                    # Use marshal to serialize the budget object
                    serialized_budgets = marshal(budgets, budget_fields)
                    print(serialized_budgets)
                    return {'message': 'Successful', 'data': serialized_budgets}
                else:
                    return {'message': 'Budgets not found'}, 404
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        