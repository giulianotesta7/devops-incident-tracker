import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate, upgrade

from .auth import auth as auth_bp
from .config import config
from .database import db
from .models import User
from .routes import bp as main_bp


def create_app():

    user = config.DB_USER
    password = config.DB_PASSWORD
    host = config.DB_HOST
    dbname = config.DB_MYSQL

    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{dbname}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    Migrate(app, db)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    if os.getenv('RUN_MIGRATIONS', 'false').lower() == 'true':
        with app.app_context():
            upgrade()

    return app

