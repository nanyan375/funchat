# -*- coding: utf-8 -*-

from flask import current_app
from flask_mail import Message

from funchat.extensions import mail
from . import celery

@celery.task(name="tasks.send")
def send(subject, recipients, body):
    msg = Message(
        subject=subject,
        recipients=recipients
        )
    msg.body = body
    mail.send(msg)
    print("-------------------send")