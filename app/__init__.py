import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../sqlite.db'
app.secret_key = Flask.secret_key


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "/loginRegister"
login_manager.init_app(app)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from main import main
from user import user
from blog import blog

app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(blog, url_prefix='/blog')

@app.route('/')
def index():
    return render_template('index.html', title="Welcome")
