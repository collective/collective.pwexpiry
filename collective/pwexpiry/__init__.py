from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
import plugin
import patches

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    registerMultiPlugin(plugin.PwExpiryPlugin.meta_type)
    context.registerClass(
        plugin.PwExpiryPlugin,
        permission=add_user_folders,
        constructors=(
            plugin.manage_addPwExpiryPluginForm,
            plugin.addPwExpiryPlugin
        ),
        visibility=None
    )