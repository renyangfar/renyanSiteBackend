import os

from flask import Flask
from user import user
from main import main

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')
