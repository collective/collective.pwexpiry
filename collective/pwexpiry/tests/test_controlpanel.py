# -*- coding: utf-8 -*-
from collective.pwexpiry.config import PROJECTNAME
from collective.pwexpiry.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'pwexpiry-controlpanel', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@pwexpiry-controlpanel')

    def test_controlpanel_installed(self):
        actions = [a.id for a in self.controlpanel.listActions()]
        self.assertIn('pwexpirycontrolpanel', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.id for a in self.controlpanel.listActions()]
        self.assertNotIn('pwexpirycontrolpanel', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)

    def test_validity_period_record_in_registry(self):
        record = 'collective.pwexpiry.validity_period'
        self.assertIn(record, self.registry)
        self.assertEqual(self.registry.get(record), 90)

    def test_notification_actions_record_in_registry(self):
        record = 'collective.pwexpiry.notification_actions'
        self.assertIn(record, self.registry)
        self.assertEqual(self.registry.get(record), None)

    def test_whitelisted_users_record_in_registry(self):
        record = 'collective.pwexpiry.whitelisted_users'
        self.assertIn(record, self.registry)
        self.assertEqual(self.registry.get(record), None)

    def test_allowed_tries_record_in_registry(self):
        record = 'collective.pwexpiry.allowed_tries'
        self.assertIn(record, self.registry)
        self.assertEqual(self.registry.get(record), 3)

    def test_disable_time_record_in_registry(self):
        record = 'collective.pwexpiry.disable_time'
        self.assertIn(record, self.registry)
        self.assertEqual(self.registry.get(record), 24)

    def test_password_history_size_record_in_registry(self):
        record = 'collective.pwexpiry.password_history_size'
        self.assertIn(record, self.registry)
        self.assertEqual(self.registry.get(record), 0)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            'collective.pwexpiry.validity_period',
            'collective.pwexpiry.notification_actions',
            'collective.pwexpiry.whitelisted_users',
            'collective.pwexpiry.allowed_tries',
            'collective.pwexpiry.disable_time',
            'collective.pwexpiry.password_history_size',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
