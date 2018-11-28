# -*- coding: utf-8 -*-

from flask_login import LoginManager
from flask_moment import Moment
from flask_oauthlib.client import OAuth
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
# from flask_celery import Celery
# from redis import Redis

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
oauth = OAuth()
mail = Mail()
# celery = Celery()
# redis = Redis()

@login_manager.user_loader
def load_user(user_id):
	from funchat.models import User
	return User.query.get(int(user_id))

login_manager.login_view = 'auth.login'
