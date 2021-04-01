from flask import Flask
from dotenv import load_dotenv
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


load_dotenv()


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
# login_manager.login_message_category = 'info'


# from flaskblog import routes  # noqa: E402


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    mail.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from flaskblog.main.routes import main  # noqa: E402
    from flaskblog.user.routes import user_routes  # noqa: E402
    from flaskblog.auth.routes import auth  # noqa: E402
    from flaskblog.post.routes import post  # noqa: E402
    from flaskblog.errors.handlers import errors  # noqa: E402

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)
    app.register_blueprint(user_routes)
    app.register_blueprint(errors)

    return app
