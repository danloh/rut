# -*- coding: utf-8 -*-
# auth  __init__

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
