from flask import url_for, flash
from werkzeug.utils import redirect

from models import User
from forms import RegistrationForm
from . import user, db


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return 'invalidate form'
    # return render_template('auth/register.html', form=form)
