import os
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

workers =  multiprocessing.cpu_count() * 2 + 1
backlog = 2048 
worker_class = 'gevent'
proc_name = 'gunicorn.proc'