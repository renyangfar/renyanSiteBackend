from flask import url_for, flash, request
from werkzeug.utils import redirect

from models import User
from . import user, db


@user.route('/register', methods=['GET', 'POST'])
def register():
    if True:
        register_data = request.form
        user = User(email=register_data.get('Email'), username=register_data.get('Username'), password=register_data.get("Password"))
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return 'invalidate form'
    # return render_template('auth/register.html', form=form)
