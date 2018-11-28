#-*- coding: utf-8 -*-

from flask import render_template, flash, redirect, Blueprint, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from funchat.extensions import db, mail
from funchat.models import User
from ..tasks import send

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('chat.home'))

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		remember_me = request.form.get('remember', False)

		if remember_me:
			remember_me = True

		user = User.query.filter_by(email=email).first()

		if user is not None:
			if user.password_hash is None:
				flash("Please use the third party service to log in")

			if user.verify_password(password):
				login_user(user, remember_me)
				return redirect(url_for('chat.home'))
		flash("Either the email or password was incorrect")
		return redirect(url_for('.login'))

	return render_template("auth/login.html")

@auth_bp.route('/logout')
@login_required
def logout():
	logout_user()
	return "<h1>You loged out</h1>"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('main.index'))

	if request.method == 'POST':
		email = request.form['email']
		user = User.query.filter_by(email=email).first()
		if user is not None:
			flash("The email is already registered, please log it in")
			return redirect(url_for('.login'))
		nickname = request.form['nickname']
		password = request.form['password']
		
		print("========================", 'here')
		subject = "Hello from FunChat"
		recipients = [email]
		body =""" 
		Dear %s,
			Welcome to FunChat, Here you can chat with friends. Hope you have fun!
		"""%nickname
		send.delay(subject, recipients, body)

		user = User(nickname=nickname, email=email)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		print("----------------------------done")
		login_user(user, remember=True)
		return redirect(url_for('.login'))

	return render_template('auth/register.html')
