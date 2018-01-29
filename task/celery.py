# -*- coding: utf-8 -*-

from celery import Celery

celery_app = Celery('task', include=['task.tasks'])
celery_app.config_from_object('task.celeryconfig')

if __name__ == '__main__':
    celery_app.start()