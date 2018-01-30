# -*- coding: utf-8 -*-
from app import mail
from .celery import celery_app
from flask import render_template
from flask_mail import Message
from manage import app  #dev or prod

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10, ignore_result=True)
def send_email(self, to, subject, template, **kwargs):
    with app.app_context():
        try:
            msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                        sender=app.config['MAIL_SENDER'], recipients=[to])
            msg.body = render_template(template + '.txt', **kwargs)
            msg.html = render_template(template + '.html', **kwargs)
            mail.send(msg)
        except Exception as exc:
            raise self.retry(exc=exc)
