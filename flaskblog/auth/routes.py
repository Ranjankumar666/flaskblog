from flaskblog import db
from flask_login import login_required, current_user, logout_user, login_user
from secrets import token_hex
from flaskblog.auth.forms import LoginForm, RegistrationForm
from flask import redirect, render_template, flash, request, url_for, Blueprint
from flaskblog.models import Post, User
import bcrypt

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()

    email, password, remember = form.email.data, form.password.data, form.remember.data

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if (user and bcrypt.checkpw(str.encode(password), str.encode(user.password))):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Hey! Welcome.....')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash(f'Password/Email is wrong')
        return redirect(url_for('auth.login'))

    return render_template('login.html', title='Login', form=form)


@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    name, email, password = form.name.data, form.email.data, form.password.data

    if form.validate_on_submit():
        password = str.encode(password)
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt(14)).decode('utf8')
        new_user = User(name=name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Account created successfully for {form.name.data}')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/auth/logout')
@ login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
