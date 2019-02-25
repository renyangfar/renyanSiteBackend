from flask import Blueprint

from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


user = Blueprint('user', __name__)
from . import views
