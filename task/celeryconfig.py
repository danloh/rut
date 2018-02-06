# -*- coding: utf-8 -*-

import os
from datetime import timedelta
from celery.schedules import crontab
imports = ['task.tasks']
broker_url = os.environ.get('BROKER_URL')
# result_backend = 
# task_serializer = ''
# result_serializer = ''
# result_expires = 
# accept_content = []
timezone = 'UTC'

## config periodic task
beat_schedule = {
    'cal_vote': {
        'task': 'task.tasks.cal_vote_celery',
        'schedule': crontab(minute=0, hour='*/2')
    }
}