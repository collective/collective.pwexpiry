import logging
from zope.component import getAdapters
from Products.CMFPlone.RegistrationTool import RegistrationTool
from collective.pwexpiry.interfaces import ICustomPasswordValidator

logger = logging.getLogger(__file__)

original_testPasswordValidity = RegistrationTool.testPasswordValidity
def extended_testPasswordValidity(self, password, confirm=None, data=None):
    """
    Patching the standard Plone's testPasswordValidity method to
    enable registering a custom password validator.
    """
    original = original_testPasswordValidity(self, password, confirm)
    if original:
        return original
    else:
        validators = getAdapters((self,), ICustomPasswordValidator)
        for name, validator in validators:
            result = validator.validate(password, data)
            if result:
                return result
    return None

RegistrationTool.testPasswordValidity = extended_testPasswordValidity
logger.info("Patching Products.CMFDefault.RegistrationTool.testPasswordValidity")


from zope.app.form.interfaces import WidgetInputError
from Products.CMFCore.utils import getToolByName
from plone.app.users.browser.register import BaseRegistrationForm

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
            original.append(WidgetInputError('password', u'label_password', error))
            self.widgets['password'].error = error
    return original

BaseRegistrationForm.validate_registration = extended_validate_registration
logger.info("Patching Products.CMFDefault.RegistrationTool.testPasswordValidity")
