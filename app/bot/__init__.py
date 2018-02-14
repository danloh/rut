# -*- coding: utf-8 -*-
# bot  __init__

from flask import Blueprint

bot = Blueprint('bot', __name__)

from . import spider
