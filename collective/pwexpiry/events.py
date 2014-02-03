from zope.component.interfaces import ObjectEvent
from zope.interface import implements

from collective.pwexpiry.interfaces import IValidPasswordEntered
from collective.pwexpiry.interfaces import IInvalidPasswordEntered


class ValidPasswordEntered(ObjectEvent):
    """A user enetered a valid password
    """
    implements(IValidPasswordEntered)


class InvalidPasswordEntered(ObjectEvent):
    """A user enetered a valid password
    """
    implements(IInvalidPasswordEntered)
