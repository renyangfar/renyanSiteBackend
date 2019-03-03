# coding=utf-8

import json
import re

from flask import request
from flask_login import login_user, logout_user, login_required

from app import db
from .models import User
from . import user


@user.route('/login', methods=['POST'])
def login():
    try:
        req_data = request.form
        username, password = req_data.get('username', ''), req_data.get('password', '')
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return json.dumps({"success": False, "data": "username or password error"})
        login_user(user)
        return json.dumps({"success": True, "data": "login success"})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        return json.dumps({"success": True, "data": 'logout success'})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})


@user.route('/register', methods=['POST'])
def register():
    try:
        req_data = request.form
	print(req_data)
        email, username, password, password_confirm = req_data.get('email', ''), req_data.get('username', ''), \
                                                      req_data.get('password', ''), req_data.get('password_confirm', '')
        if not len(username) >= 4:
            return json.dumps({"success": False, "data": "invalid username format"})
        if not len(password) >= 4:
            return json.dumps({"success": False, "data": "invalid password format"})
        if not password == password_confirm:
            return json.dumps({"success": False, "data": "invalid password_confirm format"})
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return json.dumps({"success": False, "data": "invalid email format"})
        if User.query.filter_by(username=username).first():
            return json.dumps({"success": False, "data": "username exist"})
        if User.query.filter_by(email=email).first():
            return json.dumps({"success": False, "data": "email exist"})
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return json.dumps({"success": True, "data": "register success"})
    except Exception as e:
        print(e)
        return json.dumps({"success": False, "data": e.message})
