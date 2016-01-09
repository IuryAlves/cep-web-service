#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import unittest
import sys
import os

if __name__ == '__main__':
    test_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    project_path = os.path.sep.join(test_path.split(os.path.sep)[:-2])
    sys.path.append(project_path)

    tests = unittest.TestLoader().discover(test_path, "*tests.py")
    result = unittest.TextTestRunner().run(tests)

    for skipped in result.skipped:
        print(skipped)

    if not result.wasSuccessful():
        sys.exit(1)
