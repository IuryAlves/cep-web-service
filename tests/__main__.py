#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import unittest
import sys
import os

if __name__ == '__main__':
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)[:-1]
    APP_PATH = os.path.sep.join(ROOT_PATH + ['src'])
    print(APP_PATH)
    if APP_PATH not in sys.path:
        sys.path.append(APP_PATH)

    try:
        tests = unittest.TestLoader().discover(sys.argv[1], "*tests.py")
    except IndexError:
        tests = unittest.TestLoader().discover('tests', "*tests.py")

    result = unittest.TextTestRunner().run(tests)

    for skipped in result.skipped:
        print(skipped)

    if not result.wasSuccessful():
        sys.exit(1)
