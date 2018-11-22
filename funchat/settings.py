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
