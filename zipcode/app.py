# coding: utf-8
from __future__ import absolute_import

from flask import Flask
from resources.zipcode.blueprint import zipcode_blueprint

app = Flask(__name__)
app.register_blueprint(zipcode_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
