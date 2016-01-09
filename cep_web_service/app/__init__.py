# coding: utf-8
from __future__ import absolute_import

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from cep_web_service import settings

app = Flask(__name__)
app.config.from_object(settings)
db = MongoEngine(app)

from .zipcode.resources import zipcode_blueprint

app.register_blueprint(zipcode_blueprint)
