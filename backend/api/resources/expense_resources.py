"""Budget resources"""
from flask_restful import Resource, reqparse, fields, marshal
from datetime import datetime
from api.models.budget_models import Budget
from api.models.expense_models import Expense
from api import db
from flask_login import current_user, login_required

    
expense_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'budget_id': fields.Integer,
    'category': fields.String,
    'amount': fields.Float(attribute=lambda x: round(x.amount, 2)),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class AllBudgetExpenses(Resource):
    """/users/id/budgets/budget_id/expenses route handler"""
    @login_required
    def post(self, id, budget_id):
        """POST /users/id/budgets/budget_id/expenses """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter_by(user_id=id, id=budget_id).first()
                if budget:
                    parser = reqparse.RequestParser()
                    parser.add_argument('category', help='This field is required', type = str, location = 'json', required=True)
                    parser.add_argument('amount', help='This field is required', type = float, location = 'json', required=True)
                    data = parser.parse_args()

                    new_expense = Expense(
                        user_id=current_user.id,
                        budget_id=budget.id,
                        category=data['category'],
                        amount=data['amount']
                    )

                    db.session.add(new_expense)
                    db.session.commit()
                    return {'message': 'Expense added successfully', 'data': data }, 201
                else:
                    return {'message': 'Budget with id - {} not found'.format(budget_id)}, 404 
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception as err:
            print(err)
            return {'message': 'An error occured, ensure you are using the right keys, datatypes and your request body is properly formatted'}, 400
