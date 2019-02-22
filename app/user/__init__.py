from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint

db = SQLAlchemy()
login_manager = LoginManager()

user = Blueprint('user', __name__)
from . import views
