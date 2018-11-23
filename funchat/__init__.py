# -*- coding: utf-8 -*-

import os
import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from funchat.blueprints.auth import auth_bp
from funchat.blueprints.chat import chat_bp
from funchat.settings import config
from funchat.extensions import db, login_manager, csrf, moment, oauth, socketio
from funchat.models import User, Message

def create_app(config_name=None):
	if config_name is None:
		config_name = os.getenv('FLASK_CONFIG', 'development')

	app = Flask('funchat')
	app.config.from_object(config[config_name])
	
	register_extensions(app)
	register_blueprints(app)
	register_errors(app)
	register_commands(app)

	return app

def register_extensions(app):
	db.init_app(app)
	login_manager.init_app(app)
	csrf.init_app(app)
	socketio.init_app(app)
	moment.init_app(app)


def register_blueprints(app):
	app.register_blueprint(auth_bp)
	app.register_blueprint(chat_bp)

def register_errors(app):
	pass

def register_commands(app):
	@app.cli.command()
	@click.option('--drop', is_flag=True, help='Create after drop')
	def initdb(drop):
		""" 初始化数据库 """
		if drop:
			click.confirm('This operation will delete the database, do you want to continue?', abort=True)
			db.drop_all()
			click.echo('Drop tables')
		db.create_all()
		click.echo("Initialized database.")

	@app.cli.command()
	@click.option('--message', default=300, help="Quantity of messages, default is 300.")
	def forge(message):
		"""生产测试数据"""
		import random
		from sqlalchemy.exc import IntegrityError
		from faker import Faker

		fake = Faker()

		click.echo("Initializing the database...")
		db.drop_all()
		db.create_all()

		click.echo("Forging the data...")
		admin = User(nickname="admin", email='admin@example.com')
		admin.set_password('123456')
		db.session.add(admin)
		db.session.commit()

		click.echo('Genarating users....')
		for i in range(50):
			user = User(
				nickname=fake.name(),
				bio=fake.sentence(),
				github=fake.url(),
				website=fake.url(),
				email=fake.email()
			)
			db.session.add(user)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()

		click.echo("Genarating messaages...")
		for i in range(message):
			message = Message(
				author = User.query.get(random.randint(1, User.query.count())),
				body = fake.sentence(),
				timestamp = fake.date_time_between('-30d', '-2d')
			)
			db.session.add(message)
		db.session.commit()
		click.echo('Done.')