# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from funchat.blueprints.auth import auth_bp
from funchat.settings import config
from funchat.extensions import db, login_manager, csrf, moment, oauth
from funchat.models import User, Message

def create_app(config_name=None):
	if config_name is None:
		config_name = os.getenv('FLASK_CONFIG', 'development')

	app = Flask('funchat')
	app.config.from_object(config[config_name])
	
	print("+++++++++++++++++++++++++")
	register_extensions(app)
	register_blueprints(app)
	register_errors(app)
	register_commands(app)

	return app

def register_extensions(app):
	db.init_app(app)
	login_manager.init_app(app)
	csrf.init_app(app)


def register_blueprints(app):
	app.register_blueprint(auth_bp)

def register_errors(app):
	pass

def register_commands(app):
	pass

