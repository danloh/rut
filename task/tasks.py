# -*- coding: utf-8 -*-
import os
from app import mail, db
from app.models import *
from flask import render_template
from flask_mail import Message
from task.celery import celery_app

dev_or_prod = os.environ.get('DEV_OR_PROD')
if dev_or_prod == 'dev':
    from manage import app
else:
    from run import app

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

@celery_app.task(ignore_result=True)
def set_event_celery(userid,action=None,postid=None,itemid=None,\
                    reviewid=None,demandid=None,tagid=None,headlineid=None):
    with app.app_context():
        user = Users.query.get(userid)
        user.set_event(action,postid,itemid,reviewid,demandid,tagid,headlineid)

@celery_app.task(ignore_result=True)
def cal_vote_celery():
    with app.app_context():
        ruts = Posts.query
        for r in ruts:
            r.cal_vote()
        tags = Tags.query
        for t in tags:
            t.cal_vote()
        headlines = Headlines.query
        for h in headlines:
            h.cal_point()
        items = Items.query
        for i in items:
            i.cal_vote()
        db.session.commit()
