"""Flask app initialization"""
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize SQLAlchemy without tying it to an app
db = SQLAlchemy()

# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Initialize SQLAlchemy with the app after app is created
db.init_app(app)

from api import routes
