# cep-web-service
A Flask web service to handle CEP data
[![Build Status](https://travis-ci.org/IuryAlves/cep-web-service.svg?branch=master)](https://travis-ci.org/IuryAlves/cep-web-service) [![Coverage Status](https://coveralls.io/repos/IuryAlves/cep-web-service/badge.svg?branch=master&service=github)](https://coveralls.io/github/IuryAlves/cep-web-service?branch=master) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


# Installing

* Install python 3
* Install virtualenv

        pip install virtualenv

* Create a virtualenv

        virtualenv venv --python=python3
        source venv/bin/activate
        
* Install requirements

        pip install -r requirements/requirements.txt
        
### You will also need to install mongodb. [Here](https://docs.mongodb.org/manual/installation/) is some good documentation about mongo installation.

After the installation you will need to create a folder to mongo store the data, usually is in /data/db

       sudo mkdir -p /data/db # unix only
       
And Start mongo

       sudo mongod
       
If you don't have sudo permissions or don't want use sudo, you can specify the ```--dbpath``` to mongo
        
        mkdir -p data/db # in any directory you like
        mongod --dbpath data/db


## Running

With virtualenv active do

    python cep_web_service/run.py