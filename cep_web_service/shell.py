#!/usr/bin/env python
# coding: utf-8
import sys
import os
import readline  # noqa
from pprint import pprint  # noqa

from flask import *  # noqa
project_path = os.path.sep.join(os.path.abspath(os.path.join(os.path.dirname(__file__))).split(os.path.sep)[:-1])
sys.path.append(project_path)
from app import *  # noqa

os.environ['PYTHONINSPECT'] = 'True'
