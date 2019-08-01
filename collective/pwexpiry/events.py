# -*- coding: utf-8 -*-

from collective.pwexpiry.interfaces import (
    IInvalidPasswordEntered,
    IUserUnlocked,
    IValidPasswordEntered,
)
from zope.component.interfaces import ObjectEvent
from zope.interface import implementer


@implementer(IValidPasswordEntered)
class ValidPasswordEntered(ObjectEvent):
    """A user enetered a valid password
    """


@implementer(IInvalidPasswordEntered)
class InvalidPasswordEntered(ObjectEvent):
    """A user enetered an invalid password
    """


@implementer(IUserUnlocked)
class UserUnlocked(object):
    """An user has been unlocked from the control panel tool
    """

    def __init__(self, user):
        self.user = user
