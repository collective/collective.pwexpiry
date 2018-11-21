# -*- coding: utf-8 -*-
from collective.pwexpiry.config import IS_PLONE_5
# from collective.pwexpiry.config import PROJECTNAME
# from collective.pwexpiry.interfaces import ICollectivePWExpiryLayer
from collective.pwexpiry.testing import ROBOT_TESTING

from plone.testing import layered

import os
import robotsuite
import unittest


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
if IS_PLONE_5:
    tests = [f for f in files if f.startswith('test_') and f.endswith('p5.robot')]
else:
    tests = [f for f in files if f.startswith('test_') and f.endswith('p4.robot')]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            robotsuite.RobotTestSuite(t,),
            layer=ROBOT_TESTING)
        for t in tests
    ])
    return suite