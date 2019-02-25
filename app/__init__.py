import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../sqlite.db'

db = SQLAlchemy(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from user import user
from main import main

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')
