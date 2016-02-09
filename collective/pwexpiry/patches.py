import logging

from AccessControl import AuthEncoding
from collective.pwexpiry.events import (InvalidPasswordEntered,
                                        ValidPasswordEntered)
from collective.pwexpiry.interfaces import ICustomPasswordValidator
from plone import api
from plone.app.users.browser.register import BaseRegistrationForm
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.RegistrationTool import RegistrationTool
from Products.PluggableAuthService.plugins.ZODBUserManager import \
    ZODBUserManager
from zope.app.form.interfaces import WidgetInputError
from zope.component import getAdapters
from zope.event import notify

try:
    from hashlib import sha1 as sha
except:
    from sha import sha



logger = logging.getLogger(__file__)


original_testPasswordValidity = RegistrationTool.testPasswordValidity


def extended_testPasswordValidity(self, password, confirm=None, data=None):
    """
    Patching the standard Plone's testPasswordValidity method to
    enable registering a custom password validator.
    """
    validators = getAdapters((self,), ICustomPasswordValidator)
    for name, validator in validators:
        result = validator.validate(password, data)
        if result:
            return result

    original = original_testPasswordValidity(self, password, confirm)
    if original:
        return original

    return None

RegistrationTool.testPasswordValidity = extended_testPasswordValidity
logger.info(
    "Patching Products.CMFDefault.RegistrationTool.testPasswordValidity"
)

original_validate_registration = BaseRegistrationForm.validate_registration


def extended_validate_registration(self, action, data):
    """
    Patching the standard Plone's validate_registration method to
    add validating the password given in the registration process against
    the testPasswordValidity method.
    (This will be added to Plone 4.3 according to https://dev.plone.org/ticket/10959)
    """
    original = original_validate_registration(self, action, data)
    pw_error = self.widgets['password'].error
    if isinstance(pw_error, str):
        return original
    elif callable(pw_error):
        registration = getToolByName(self.context, 'portal_registration')
        password = data.get('password')
        confirm = data.get('password_ctl')
        error = registration.testPasswordValidity(password, confirm, data)
        if error:
            original.append(
                WidgetInputError('password', u'label_password', error)
            )
            self.widgets['password'].error = error
    return original

BaseRegistrationForm.validate_registration = extended_validate_registration
logger.info(
    "Patching plone.app.users.browser.register.BaseRegistrationForm.validate_registration")


ZODBUserManager.original_authenticateCredentials = ZODBUserManager.authenticateCredentials


def authenticateCredentials(self, credentials):
    """ See IAuthenticationPlugin.

    o We expect the credentials to be those returned by
      ILoginPasswordExtractionPlugin.
    """
    login = credentials.get('login')
    password = credentials.get('password')

    if login is None or password is None:
        return None

    # Do we have a link between login and userid?  Do NOT fall
    # back to using the login as userid when there is no match, as
    # that gives a high chance of seeming to log in successfully,
    # but in reality failing.
    userid = self._login_to_userid.get(login)
    if userid is None:
        # Someone may be logging in with a userid instead of a
        # login name and the two are not the same.  We could try
        # turning those around, but really we should just fail.
        #
        # userid = login
        # login = self._userid_to_login.get(userid)
        # if login is None:
        #     return None
        return None

    reference = self._user_passwords.get(userid)

    if reference is None:
        return None

    is_authenticated = False
    if AuthEncoding.is_encrypted(reference):
        if AuthEncoding.pw_validate(reference, password):
            is_authenticated = True

    if not is_authenticated:
        # Support previous naive behavior
        digested = sha(password).hexdigest()

        if reference == digested:
            is_authenticated = True

    if is_authenticated:
        try:
            user = api.user.get(username=login)
        except:
            return userid, login

        event = ValidPasswordEntered(user)
        notify(event)
        return userid, login
    else:
        try:
            user = api.user.get(username=login)
        except:
            return None

        event = InvalidPasswordEntered(user)
        notify(event)
        return None

ZODBUserManager.authenticateCredentials = authenticateCredentials
logger.info("Patching Products.PluggableAuthService.plugins.ZODBUserManager."
            "ZODBUserManager.authenticateCredentials")
