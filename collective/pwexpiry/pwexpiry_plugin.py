# -*- coding: utf-8 -*-

from DateTime import DateTime
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from AccessControl.SecurityManagement import noSecurityManager

from zope.component import getUtility
from zope.interface import implements
from plone import api
from plone.registry.interfaces import IRegistry
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin, \
    IChallengePlugin
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from collective.pwexpiry.utils import days_since_event
from collective.pwexpiry.config import _

manage_addPwExpiryPluginForm = PageTemplateFile('www/addPwExpiryPlugin',
    globals(), __name__='manage_addPwExpiryPlugin')

def addPwExpiryPlugin(self, id, title='', REQUEST=None):
    """
    Add PwExpiry plugin
    """
    o = PwExpiryPlugin(id, title)
    self._setObject(o.getId(), o)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_main'
            '?manage_tabs_message=PwExpiry+Plugin+added.' %
            self.absolute_url())


class PwExpiryPlugin(BasePlugin):
    """
    Password expiry plugin
    """
    meta_type = 'Password Expiry Plugin'
    security = ClassSecurityInfo()
    implements(IAuthenticationPlugin, IChallengePlugin, IUserManagement)

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    # IAuthenticationPlugin implementation
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """
        Authenticate credentials
        """
        login = credentials.get('login')
        if not login:
            return None

        self._invalidatePrincipalCache(login)
        user = api.user.get(username=login)
        if not user:
            return None

        # Ignore Managers
        if user.has_role('Manager'):
            return None

        password_date = user.getProperty('password_date', '2000/01/01')
        if str(password_date) != '2000/01/01':
            current_time = DateTime()
            registry = getUtility(IRegistry)
            validity_period = registry['collective.pwexpiry.validity_period']
            since_last_pw_reset = days_since_event(password_date.asdatetime(),
                                                   current_time.asdatetime())
            # Password has expired
            if validity_period - since_last_pw_reset < 0:
                self.REQUEST.RESPONSE.setHeader('user_expired', user.getId())
                raise Unauthorized
        return None

    # IChallengePlugin implementation
    security.declarePrivate('challenge')
    def challenge(self, request, response, **kw):
        """
        Challenge the user for credentials
        """
        user_expired = response.getHeader('user_expired')
        if user_expired:
            portal_url = api.portal.get_tool(name='portal_url')()
            IStatusMessage(request).add(_(u'Your password has expired.'), type='warning')
            response.redirect('%s/mail_password_form?userid=%s' % (portal_url, user_expired), lock=1)
            return 1
        return 0

    # IUserManagement implementation
    security.declarePrivate('doChangeUser')
    def doChangeUser(self, principal_id, password):
        """
        Update user's password date
        """
        user = api.user.get(username=principal_id)
        portal = api.portal.get()
        current_time = portal.ZopeTime()
        user.setMemberProperties({'password_date': current_time})
        self._invalidatePrincipalCache(principal_id)

InitializeClass(PwExpiryPlugin)
