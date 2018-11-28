# -*- coding: utf-8 -*-

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 判断操作系统
WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:////'

class BaseConfig:
	# 每一页的项目数
	FUNCHAT_MESSAGE_PER_PAGE = 30
	# 管理员邮箱
	FUNCHAT_ADMIN_EMAIL = os.getenv('FUNCHAT_ADMIN_EMAIL', 'admin@example.com')
	SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix+os.path.join(basedir, 'data.db'))
	# 不追踪对象的修改并且发送信号
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# flask_mail相关设定
	MAIL_SUPPRESS_SEND = False
	MAIL_SERVER = 'smtp.qq.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
	MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
	# celery相关设定
	CELERY_BROKER_URL = 'redis://localhost:6379/0'
	CELERY_RESULT_BACKEND = 'redis://loaclhost:6379/0'
	CELERY_IMPORTS = ('funchat.tasks')

class DevelopmentConfig(BaseConfig):
	DEBUG = False
	# 调试DebugToolBar不拦截重定向
	DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProductionConfig(BaseConfig):
	pass

class TestingConfig(BaseConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'
	WTF_CSRF_ENABLED = False

config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}
