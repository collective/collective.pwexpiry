import doctest
import unittest2 as unittest

from Testing import ZopeTestCase as ztc
from plone.testing import layered

from collective.pwexpiry.tests import base

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(
                'tests/test1.txt',
#                'tests/test2.txt',
                package='collective.pwexpiry',
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
                layer=base.INTEGRATION_TESTING),
        ])
    return suite
