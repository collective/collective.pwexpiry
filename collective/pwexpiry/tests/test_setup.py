# -*- coding: utf-8 -*-
from collective.pwexpiry.config import IS_PLONE_5
from collective.pwexpiry.config import IS_PLONE_5_2
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
        if IS_PLONE_5_2:
            request = self.layer["request"]
            installer_view = api.content.get_view(
                u"installer", self.portal, request
            )
            self.assertTrue(installer_view.is_product_installed(PROJECTNAME))
        else:
            qi = self.portal["portal_quickinstaller"]
            self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(ICollectivePWExpiryLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, "Plone 4.3 only")
    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5_2, "Not needed for Plone 5.2")
    def test_skin(self):
        skins = self.portal["portal_skins"]
        self.assertIn("pwexpiry", skins)


class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if IS_PLONE_5_2:
            request = self.layer["request"]
            installer_view = api.content.get_view(
                u"installer", self.portal, request
            )
            installer_view.uninstall_product(PROJECTNAME)
        else:
            self.qi = self.portal["portal_quickinstaller"]

            with api.env.adopt_roles(["Manager"]):
                self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        if IS_PLONE_5_2:
            request = self.layer["request"]
            installer_view = api.content.get_view(
                u"installer", self.portal, request
            )
            self.assertFalse(installer_view.is_product_installed(PROJECTNAME))
        else:
            self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(ICollectivePWExpiryLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, "Plone 4.3 only")
    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertNotIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5_2, "Not needed for Plone 5.2")
    def test_skin_removed(self):
        skins = self.portal["portal_skins"]
        self.assertNotIn("pwexpiry", skins)
