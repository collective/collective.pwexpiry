# -*- coding: utf-8 -*-
from collective.pwexpiry.config import _
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.login.login import LoginForm
from Products.CMFPlone import PloneMessageFactory as PMF_
from Products.CMFPlone.interfaces import ILoginForm
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope.interface import implementer


@implementer(ILoginForm)
class PWExpiryLoginForm(LoginForm):
    """
    """

    @button.buttonAndHandler(PMF_("Log in"), name="login")
    def handleLogin(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        membership_tool = getToolByName(self.context, "portal_membership")
        status_msg = IStatusMessage(self.request)
        if membership_tool.isAnonymousUser():
            self.request.response.expireCookie("__ac", path="/")
            if self.use_email_as_login():
                status_msg.addStatusMessage(
                    _(
                        u"Login failed. Both email address and password are "
                        u"case sensitive, check that caps lock is not "
                        u"enabled. If you have entered your password "
                        u"correctly, your account might be locked. You can "
                        u"reset your password, or contact an administrator "
                        u"to unlock it, using the Contact form."
                    ),
                    type="error",
                )
            else:
                status_msg.addStatusMessage(
                    _(
                        u"Login failed. Both login name and password are "
                        u"case sensitive, check that caps lock is not "
                        u"enabled. If you have entered your password "
                        u"correctly, your account might be locked. You can "
                        u"reset your password, or contact an administrator "
                        u"to unlock it, using the Contact form."
                    ),
                    type="error",
                )
            return

        is_initial_login = self._post_login()
        status_msg.addStatusMessage(
            PMF_(
                u"you_are_now_logged_in",
                default=u"Welcome! You are now logged in.",
            ),
            "info",
        )

        came_from = data.get("came_from", None)
        self.redirect_after_login(came_from, is_initial_login)


class PWExpiryFailsafeLoginForm(PWExpiryLoginForm):
    def render(self):
        return self.index()
