import unittest
from flask import Flask
from api import db
from api.models.user_models import User

class TestUserModel(unittest.TestCase):
    """Test cases for user model"""

    def setUp(self):
        """Set up a test database"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the test database"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        # Test creating a new user
        user = User(firstname='John', lastname='Doe', email='john@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)
        self.assertEqual(user.rank, 0)
        self.assertEqual(user.firstname, 'John')
        self.assertEqual(user.lastname, 'Doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_update_user(self):
        # Test updating user information
        user = User(firstname='John', lastname='Doe', email='john@example.com', password='password123')
        db.session.add(user)
        db.session.commit()

        # Update user information
        user.rank = 1
        user.firstname = 'Jane'
        user.lastname = 'Doe'
        user.email = 'jane@example.com'
        db.session.commit()

        self.assertEqual(user.rank, 1)
        self.assertEqual(user.firstname, 'Jane')
        self.assertEqual(user.lastname, 'Doe')
        self.assertEqual(user.email, 'jane@example.com')
        self.assertIsNotNone(user.updated_at)

    def test_user_repr_method(self):
        # Test the __repr__ method
        user = User(firstname='John', lastname='Doe', email='john@example.com', password='password123')
        self.assertEqual(repr(user), "User('John', 'Doe', 'john@example.com')")

    def test_default_values(self):
        # Test default values of User model
        new_user = User()
        self.assertEqual(new_user.rank, 0)
        self.assertIsNotNone(new_user.created_at)
        self.assertIsNotNone(new_user.updated_at)

    def test_unique_constraint(self):
        # Test unique constraint on email field
        user1 = User(firstname='John', lastname='Doe', email='john@example.com', password='password123')
        user2 = User(firstname='Jane', lastname='Doe', email='john@example.com', password='anotherpassword')
        db.session.add(user1)
        db.session.commit()
        with self.assertRaises(Exception):
            db.session.add(user2)
            db.session.commit()

    def test_password_hashing(self):
        # Test password hashing
        password = 'securepassword'
        user = User(firstname='John', lastname='Doe', email='john@example.com', password=password)
        db.session.add(user)
        db.session.commit()
        self.assertNotEqual(user.password, password)

if __name__ == '__main__':
    unittest.main()
