from flaskblog import db
from flask_login import login_required, current_user
from secrets import token_hex
from PIL import Image
from flaskblog.user.forms import UpdateProfileForm
from flask import redirect, render_template, flash, request, url_for, Blueprint, current_app
from flaskblog.models import Post, User
import os
from os import path


user_routes = Blueprint('user_routes', __name__)


def save_file(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = path.join(
        current_app.root_path, 'static/profile-pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


@user_routes.route('/user/profile/<id>', methods=['GET'])
def user_profile(id):
    page = request.args.get('page', default=1, type=1)
    user = User.query.get(id)
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(per_page=5, page=page)

    image_file = url_for(
        'static', filename="profile-pictures/"+user.image_file)
    return render_template('user_profile.html', user=user, image_file=image_file, posts=posts)


@user_routes.route('/user/<id>', methods=['GET', 'POST'])
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
