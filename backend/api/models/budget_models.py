"""Budget model"""
from datetime import datetime
from api import db


class Budget(db.Model):
    """Budget model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(300), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    start = db.Column(db.String(120), nullable=False)
    end = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"Budget('{self.name}', '{self.amount}', '{self.start}', '{self.end}')"
