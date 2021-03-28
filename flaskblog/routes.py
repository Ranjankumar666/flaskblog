from flaskblog.models import User, Post  # noqa: E402
from flask import render_template, redirect, flash, url_for, session, request
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog import app, db
from flask_login import login_user, logout_user, current_user, login_required
import bcrypt


@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home Page')

    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('home.html', title='About')


@app.route('/posts')
def about_post():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts, title='Posts')


@app.route('/user/<id>')
@login_required
def user(id):
    return render_template('account.html', title=f'Welcome {current_user.name} ')


@app.route('/auth/login', methods=["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    email, password, remember = form.email.data, form.password.data, form.remember.data

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if (user and bcrypt.checkpw(str.encode(password), str.encode(user.password))):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Hey! Welcome.....')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash(f'Password/Email is wrong')
        return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
