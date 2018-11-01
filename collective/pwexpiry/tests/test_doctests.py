# -*- coding: utf-8 -*-
from collective.pwexpiry.testing import INTEGRATION_TESTING
from plone.testing import layered

import doctest
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(
                'tests/test.txt',
                package='collective.pwexpiry',
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
                layer=INTEGRATION_TESTING),
    ])
    return suite
