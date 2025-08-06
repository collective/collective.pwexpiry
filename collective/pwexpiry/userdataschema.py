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
        title=_("label_password_date", default="Password date"),
        description=_(
            "help_password_date", default="The date of setting the password"
        ),
        required=False,
    )

    last_notification_date = schema.Date(
        title=_(
            "label_last_notification_date", default="Last notification date"
        ),
        description=_(
            "help_last_notification_date",
            default=(
                "The date of performing the last notification for the user"
            ),
        ),
        required=False,
    )
