"""Expense model"""
from datetime import datetime
from api import db


class Expense(db.Model):
    """Expense model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(precision=20, scale=2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"Expense('{self.category}', '{self.amount}')"
