from flaskblog.models import User, Post  # noqa: E402
from flask import render_template, redirect, flash, url_for, session, request
from flaskblog.form import RegistrationForm, LoginForm, UpdateProfileForm, NewPostForm, UpdatePostForm, DeletePostForm
from flaskblog import app, db
from flask_login import login_user, logout_user, current_user, login_required
from os import path
from PIL import Image
import os
import bcrypt
import secrets


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', type=int, default=1)

    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', title='Home Page', posts=posts)
    # if current_user.is_authenticated:

    # return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('home.html', title='About')


# @app.route('/posts')
# def about_post():
#     posts = Post.query.all()
#     return render_template('posts.html', posts=posts, title='Posts')


def save_file(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = path.join(
        app.root_path, 'static/profile-pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


@app.route('/user/profile/<id>', methods=['GET'])
def user_profile(id):
    page = request.args.get('page', default=1, type=1)
    user = User.query.get(id)
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(per_page=5, page=page)

    image_file = url_for(
        'static', filename="profile-pictures/"+user.image_file)
    return render_template('user_profile.html', user=user, image_file=image_file, posts=posts)


@app.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    form = UpdateProfileForm()
    email, name = form.email.data, form.name.data

    if form.validate_on_submit():
        current_user.email = email
        current_user.name = name
        file = request.files['picture']
        if file:
            # remove the old image and add the new image path
            filepath = path.join(
                app.root_path, 'static/profile-pictures', current_user.image_file)
            if path.exists(filepath):
                os.remove(filepath)
            uploaded_path = save_file(file)
            current_user.image_file = uploaded_path

        db.session.commit()
        flash('Account info updated successfully')
        return redirect(f'/user/{current_user.id}')
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename="profile-pictures/"+current_user.image_file)
    return render_template('account.html', title=f'Welcome {current_user.name}', image_file=image_file, form=form)


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


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = NewPostForm()
    title, content = form.title.data, form.content.data
    if form.validate_on_submit():
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create_post.html', title='Create A New Post', form=form)


@app.route('/post/<id>', methods=['GET', 'POST'])
def get_post(id):
    post = Post.query.get(id)
    # form = NewPostForm()
    # title, content = form.title.data, form.content.data
    # if form.validate_on_submit():
    #     new_post = Post(title=title, content=content, user_id=current_user.id)
    #     db.session.add(new_post)
    #     db.session.commit()
    #     return redirect(url_for('home'))

    return render_template('post.html', title=post.title, post=post)


@app.route('/post/update/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def update_post(id):
    post = Post.query.get(id)
    form = UpdatePostForm()
    delete_form = DeletePostForm()

    title, content = form.title.data, form.content.data

    if request.method == 'POST':
        post.title = title
        post.content = content
        db.session.commit()
        flash('Successfully Updated Your Post')
        return redirect(f'/post/update/{id}')

    form.title.data = post.title
    form.content.data = post.content
    return render_template('update_post.html', title=post.title, post=post, form=form, delete=delete_form)


@app.route("/post/delete", methods=['POST'])
@login_required
def delete_post():
    id = request.args.get("id")
    post = Post.query.get(id)

    if current_user.id == post.author.id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))

    return 'Error'
