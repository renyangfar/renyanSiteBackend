import json
import re

from flask import request

from app import db
from .models import User
from . import user


@user.route('/register', methods=['GET', 'POST'])
def register():
    try:
        req_data = request.form
        email, username, password, password_confirm = req_data.get('email', ''), req_data.get('username', ''), \
                                                      req_data.get('password', ''), req_data.get('password_confirm', '')
        if not (email and username and password and password_confirm):
            return json.dumps({"success": False, "data": "invalid field"})
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return json.dumps({"success": False, "data": "invalid email format"})
        if not len(username) >= 4:
            return json.dumps({"success": False, "data": "invalid username format"})
        if not len(password) >= 4:
            return json.dumps({"success": False, "data": "invalid password format"})
        if not password == password_confirm:
            return json.dumps({"success": False, "data": "invalid password_confirm format"})
        if User.query.filter_by(username=username).first():
            return json.dumps({"success": False, "data": "username exist"})
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return json.dumps({"success": True, "data": "register success"})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})
