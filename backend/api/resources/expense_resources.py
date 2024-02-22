"""Budget resources"""
from flask_restful import Resource, reqparse, fields, marshal
from api.models.budget_models import Budget
from api.models.expense_models import Expense
from api import db
from flask_login import current_user, login_required
from api.resources.budget_resources import budget_fields

    
expense_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'budget_id': fields.Integer,
    'category': fields.String,
    'amount': fields.Float(attribute=lambda x: round(x.amount, 2)),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class AllBudgetsAndCorrespondingExpenses(Resource):
    """/users/id/budgets-expenses route handler"""
    @login_required
    def get(self, id):
        """GET /users/id/budgets-expenses"""
        try:
            if current_user.id == id or current_user.rank == 1:
                budgets = Budget.query.filter_by(user_id=id).all()
                if budgets:
                    # Use marshal to serialize the budgets and their corresponding expenses
                    serialized_data = []
                    for budget in budgets:
                        expenses = Expense.query.filter_by(user_id=id, budget_id=budget.id).all()
                        serialized_data.append({
                            'budget': marshal(budget, budget_fields),
                            'expenses': marshal(expenses, expense_fields)
                        })
                    return {'message': 'Successful', 'data': serialized_data}
                else:
                    return {'message': 'No budgets found for the user'}, 404
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
           
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500


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


    @login_required
    def get(self, id, budget_id):
        """GET /users/id/budgets/<int:budget_id>/expense """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter_by(user_id=id, id=budget_id).first()
                if budget:
                    expenses = Expense.query.filter_by(user_id=id, budget_id=budget_id).all()
                    if expenses:
                        # Use marshal to serialize the budget object
                        serialized_expenses = marshal(expenses, expense_fields)
                        return {'message': 'Successful', 'data': serialized_expenses}
                    else:
                        return {'message': 'No expense attached to this budget currently'}, 404
                else:
                    return {'message': 'Budgets not found'}, 404
            else:
                return {'message': "You do not have permission to perform this operation"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        

    
class Expenses(Resource):
    """/users/<int:id>/budgets/<int:budget_id>/expenses/<int:expense_id> route handler"""
    @login_required
    def get(self, id, budget_id, expense_id):
        """GET /users/<int:id>/budgets/<int:budget_id>/expenses/<int:expense_id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter_by(user_id=id, id=budget_id).first()
                if budget:
                    expenses = Expense.query.filter_by(user_id=id, budget_id=budget_id, id=expense_id).first()
                    if expenses:
                        # Use marshal to serialize the expense object
                        serialized_expense = marshal(expenses, expense_fields)
                        return {'message': 'Successful', 'data': serialized_expense}
                    else:
                        return {'message': 'Expense not found'}, 404
                else:
                    return {'message': 'Budget not found'}, 404
            else:
                return {'message': "You are trying to access another user's expense"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again!'}, 500
        
    @login_required
    def put(self, id, budget_id, expense_id):
        """ PUT /users/<int:id>/budgets/<int:budget_id>/expenses/<int:expense_id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter_by(user_id=id, id=budget_id).first()
                if budget:
                    expense = Expense.query.filter_by(user_id=id, budget_id=budget_id, id=expense_id).first()
                    if expense:
                        parser = reqparse.RequestParser()
                        parser.add_argument('category', help='This field is required', type = str, location = 'json')
                        parser.add_argument('amount', help='This field is required', type = float, location = 'json')
                        data = parser.parse_args()

                        if data['category']:
                            expense.category = data['category']
                        if data['amount']:
                            expense.amount = data['amount']

                        db.session.commit()
                        return {'message': 'Expense updated successfully', 'data': {k: v for k, v in data.items() if v is not None}}
                    else:
                        return {'message': 'Expense not found'}, 404
                else:
                    return {'message': 'Budget not found'}, 404

            else:
                return {'message': "You are not authorized to update this Expense"}, 403
        except Exception as err:
            print(err)
            return {'message': 'An error occured, ensure you are using the right keys, datatypes and your request body is properly formatted'}, 400
        
    @login_required
    def delete(self, id, budget_id, expense_id):
        """DELETE /users/<int:id>/budgets/<int:budget_id>/expense/<int:expense_id> """
        try:
            if current_user.id == id or current_user.rank == 1:
                budget = Budget.query.filter_by(user_id=id, id=budget_id).first()
                if budget:
                    expense = Expense.query.filter_by(user_id=id, budget_id=budget_id, id=expense_id).first()
                    if expense:
                        db.session.delete(expense)
                        db.session.commit()
                        return {'message': 'Expense Deleted Successfully', 'data': {'id': expense.id }}
                    else:
                        return {'message': 'Expense not found'}, 404
                else:
                    return {'message': 'Budget not found'}, 404
            else:
                return {'message': "You are trying to access another user's expense"}, 403
        except Exception as err:
            print(err)
            return {'message': 'Something went wrong, try again, ensure your request is correct!'}, 500
