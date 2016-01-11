# coding: utf-8
from __future__ import absolute_import

from logging import config, getLogger
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from cep_web_service import settings

app = Flask(__name__)
app.config.from_object(settings)
db = MongoEngine(app)
config.dictConfig(settings.LOGGING)

app.info_logger = getLogger('api.info')
app.error_logger = getLogger('api.error')

from .zipcode.resources import zipcode_blueprint

app.register_blueprint(zipcode_blueprint)
