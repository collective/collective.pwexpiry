import os

import unittest2 as unittest
from plone.app.testing import (PLONE_FIXTURE, TEST_USER_ID, TEST_USER_NAME,
                               FunctionalTesting, IntegrationTesting,
                               PloneSandboxLayer, applyProfile, login,
                               setRoles)
from Products.CMFCore.utils import getToolByName


class PwExpiryLayer(PloneSandboxLayer):
    """
    Testing layer for collective.pwexpiry
    """

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """
        Set up Zope
        """
        # Load ZCML
        import collective.pwexpiry
        self.loadZCML(package=collective.pwexpiry)
        self.loadZCML(package=collective.pwexpiry, name='overrides.zcml')

        from OFS.Application import install_package
        install_package(app, collective.pwexpiry, collective.pwexpiry.initialize)

    def setUpPloneSite(self, portal):
        """
        Set up Plone
        """
        # import default profile
        applyProfile(portal, 'collective.pwexpiry:default')

        # Create test content
        # 1. Login as user with Manager privilages
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        """
        Tear down Zope
        """
        pass

FIXTURE = PwExpiryLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PwExpiryLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PwExpiryLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING

class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
