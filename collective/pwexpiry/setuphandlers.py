# -*- coding: utf-8 -*-
from collective.pwexpiry.logger import logger
from collective.pwexpiry.pwdisable_plugin import addPwDisablePlugin
from collective.pwexpiry.pwexpiry_plugin import addPwExpiryPlugin
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable

from Products.PlonePAS.setuphandlers import activatePluginInterfaces
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):  # pragma: no cover
    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            "collective.pwexpiry:uninstall",
            "collective.pwexpiry:robot_testing",
            "collective.pwexpiry.upgrades:0001_to_0002",
            "collective.pwexpiry.upgrades:0002_to_0003",
            "collective.pwexpiry.upgrades:0003_to_0004",
        ]


def import_various(context):
    """
    Install the PwExpiryPlugin
    """
    if context.readDataFile("collective_pwexpiry_default.txt") is None:
        return
    portal = context.getSite()

    acl = getToolByName(portal, "acl_users")
    installed = acl.objectIds()

    if "pwexpiry" not in installed:
        addPwExpiryPlugin(acl, "pwexpiry", "PwExpiry Plugin")
        activatePluginInterfaces(portal, "pwexpiry")
        for i in range(len(acl.plugins.listPluginIds(IChallengePlugin))):
            acl.plugins.movePluginsUp(IChallengePlugin, ["pwexpiry"])
    else:
        logger.info("pwexpiry already installed")

    if "pwdisable" not in installed:
        addPwDisablePlugin(acl, "pwdisable", "PwDisable Plugin")
        activatePluginInterfaces(portal, "pwdisable")
        for i in range(len(acl.plugins.listPluginIds(IChallengePlugin))):
            acl.plugins.movePluginsUp(IChallengePlugin, ["pwdisable"])
    else:
        logger.info("pwdisable already installed")
