from flaskblog import db
from flask_login import login_required, current_user, logout_user, login_user, login_required
from secrets import token_hex
from flaskblog.post.forms import NewPostForm, UpdatePostForm
from flask import redirect, render_template, flash, request, url_for, Blueprint
from flaskblog.models import Post, User
import bcrypt


post = Blueprint('post', __name__)


@ post.route('/post/create', methods=['GET', 'POST'])
@ login_required
def create_post():
    form = NewPostForm()
    title, content = form.title.data, form.content.data
    if form.validate_on_submit():
        new_post = Post(title=title, content=content,
                        user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='Create A New Post', form=form)


@ post.route('/post/<id>', methods=['GET', 'POST'])
def get_post(id):
    post = Post.query.get(id)
    return render_template('post.html', title=post.title, post=post)


@ post.route('/post/update/<id>', methods=['GET', 'POST', 'DELETE'])
@ login_required
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
    return render_template('update_post.html', title=post.title, post=post, form=form)


@ post.route("/post/delete")
@ login_required
def delete_post():
    id = request.args.get("id")
    post = Post.query.get(id)

    if current_user.id == post.author.id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.home'))

    return 'Error', 403
