# -*- coding: utf-8 -*-
from collective.pwexpiry.config import PROJECTNAME
from collective.pwexpiry.interfaces import ICollectivePWExpiryLayer
from collective.pwexpiry.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


JS = "++resource++collective.pwexpiry.fix_login_popup.js"


class InstallTestCase(unittest.TestCase):
    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_installed(self):
        request = self.layer["request"]
        installer_view = api.content.get_view(
            "installer", self.portal, request
        )
        self.assertTrue(installer_view.is_product_installed(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(ICollectivePWExpiryLayer, registered_layers())


class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        request = self.layer["request"]
        installer_view = api.content.get_view(
            "installer", self.portal, request
        )
        installer_view.uninstall_product(PROJECTNAME)

    def test_uninstalled(self):
        request = self.layer["request"]
        installer_view = api.content.get_view(
            "installer", self.portal, request
        )
        self.assertFalse(installer_view.is_product_installed(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(ICollectivePWExpiryLayer, registered_layers())
