# -*- coding: utf-8 -*-

import os
from celery.schedules import crontab
# #general config
imports = ['task.tasks']
worker_max_tasks_per_child = 50
broker_url = os.environ.get('BROKER_URL')
# result_backend =
# task_serializer = ''
# result_serializer = ''
# result_expires =
# accept_content = []

# #config routing
task_routes = {'task.tasks.send_mail': {'queue': 'mail'}}
# task_queue =

# # config periodic task
timezone = 'UTC'
beat_schedule = {
    'cal_vote': {
        'task': 'task.tasks.cal_vote_celery',
        'schedule': crontab(minute=0, hour='*/2')
    }
}
