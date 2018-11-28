#-*- coding: utf-8 -*-

import os
from funchat import create_app, celery
# from celery import Celery

# def make_celery(app):
#     """
#     integrate Celery with Flask
#     http://flask.pocoo.org/docs/0.10/patterns/celery/#configuring-celery
#     """
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
#                     backend=app.config['CELERY_RESULT_BACKEND'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task

#     class ContextTask(TaskBase):
#         abstract = True

#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery

#env = os.environ.get('BLOG_ENV', 'dev')
app = create_app()
app.app_context().push()
# 1. Each celery process needs to create an instance of the Flask application.
# 2. Register the celery object into the app object.
# celery = make_celery(flask_app)
# from funchat.extensions import celery