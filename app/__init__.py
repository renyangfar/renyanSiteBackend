from flask import Flask
from main import main

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')