from flaskblog import db, mail
from flask_login import login_required, current_user, logout_user, login_user
from secrets import token_hex
from flaskblog.main.forms import RequestResetForm, ResetPasswordForm
from flask import redirect, render_template, flash, request, url_for, Blueprint
from flaskblog.models import Post, User
import bcrypt
from flask_mail import Message


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', type=int, default=1)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', title='Home Page', posts=posts)
# if current_user.is_authenticated:

# return redirect(url_for('login'))


@main.route('/about')
def about():
    return render_template('home.html', title='About')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
        Click the link to reset your account password: \n
{url_for('main.reset_password', token=token, _external=True)}

if you didn't request the reset, Ignore it
    '''

    mail.send(msg)


@main.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    email = form.email.data

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        print(user)
        send_reset_email(user)
        flash('Email sent, check your email for the the reset link')
        return redirect(url_for('auth.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@main.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Invalid or Expired reset token')
        return redirect(url_for('main.reset_request'))

    form = ResetPasswordForm()
    password = form.password.data

    if form.validate_on_submit():
        password = str.encode(password)
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt(14)).decode('utf8')
        user.password = hashed_pw
        db.session.commit()
        flash('Password successfully changed')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)
