from flask import Flask
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.secret_key = "{}".format(os.getenv('SECRET_KEY'))

from app import routes