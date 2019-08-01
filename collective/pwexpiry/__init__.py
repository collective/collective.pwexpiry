from AccessControl.Permissions import add_user_folders
from AccessControl import allow_module
from Products.PluggableAuthService.PluggableAuthService import (
    registerMultiPlugin,
)
from . import pwexpiry_plugin
from . import pwdisable_plugin


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    allow_module("collective.pwexpiry.config")

    registerMultiPlugin(pwexpiry_plugin.PwExpiryPlugin.meta_type)
    context.registerClass(
        pwexpiry_plugin.PwExpiryPlugin,
        permission=add_user_folders,
        constructors=(
            pwexpiry_plugin.manage_addPwExpiryPluginForm,
            pwexpiry_plugin.addPwExpiryPlugin,
        ),
        visibility=None,
    )

    registerMultiPlugin(pwdisable_plugin.PwDisablePlugin.meta_type)
    context.registerClass(
        pwdisable_plugin.PwDisablePlugin,
        permission=add_user_folders,
        constructors=(
            pwdisable_plugin.manage_addPwDisablePluginForm,
            pwdisable_plugin.addPwDisablePlugin,
        ),
        visibility=None,
    )
