# -*- coding: utf-8 -*-
from collective.pwexpiry.config import _
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implementer


@implementer(IUserDataSchemaProvider)
class UserDataSchemaProvider(object):

    def getSchema(self):
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """Use all the fields from the default user data schema, and add
    extra field for the date of password set.
    """
    password_date = schema.Date(
        title=_(u'label_password_date', default=u'Password date'),
        description=_(
            u'help_password_date',
            default=u'The date of setting the password'),
        required=False,
    )

    last_notification_date = schema.Date(
        title=_(
            u'label_last_notification_date',
            default=u'Last notification date'),
        description=_(
            u'help_last_notification_date',
            default=u'The date of performing the last notification for the user'),
        required=False,
    )
