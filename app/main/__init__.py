# -*- coding: utf-8 -*-
# main  __init__

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors   #current package

