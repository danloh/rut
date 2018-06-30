# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from app import mail, db
from app.models import (
    Users, Posts, Tags, Items, Demands, Reviews, Articles, Events, Heat)
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
def set_event_celery(userid, action=None, postid=None, itemid=None, reviewid=None, 
                     demandid=None, clipid=None, tagid=None, articleid=None):
    with app.app_context():
        user = Users.query.get(userid)
        user.set_event(action=action, postid=postid, itemid=itemid, reviewid=reviewid,
                demandid=demandid, clipid=clipid, tagid=tagid, articleid=articleid)


@celery_app.task(ignore_result=True)
def cal_vote_celery():
    """need to narrow the query"""
    with app.app_context():
        ruts = Posts.query
        for r in ruts:
            r.cal_vote()
        tags = Tags.query
        for t in tags:
            t.cal_vote()
        items = Items.query
        for i in items:
            i.cal_vote()
        demands = Demands.query
        for d in demands:
            d.cal_point()
        reviews = Reviews.query
        for rv in reviews:
            rv.cal_point()
        articles = Articles.query
        for h in articles:
            h.cal_point()
        db.session.commit()

@celery_app.task(ignore_result=True)
def event_heat_celery():
    day = datetime.utcnow().date() - timedelta(days=1) # one day delay
    with app.app_context():
        ev_lst = Events.to_heat(day)
        Heat.into_heat(ev_lst)
