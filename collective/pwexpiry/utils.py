# -*- coding: utf-8 -*-
import pytz
from collective.pwexpiry.config import _
from plone import api
from zope.i18n import translate


template_subject = _(
    "email_subject",
    default='${days} days left to password expiration'
)

template_email_text = _("email_text", default="""Hello ${username},

There are ${days} days left before your password expires!

Please ensure to reset your password before it's expired.
""")

template_email_text_expired = _("email_text_expired", default="""Hello ${username},

Your password has expired.

Please ensure to reset your password before it's expired.
""")


def send_notification_email(user, days_to_expire):
    """
    """

    language = api.portal.get_default_language()
    if user.getProperty('language'):
        language = user.getProperty('language')

    recipient = user.getProperty('email')

    msg_mapping = {
        u"username": user.getProperty('fullname'),
        u"days": days_to_expire,
    }
    if days_to_expire > 0:
        msg = translate(
            template_email_text,
            mapping=msg_mapping,
            target_language=language
        )
    else:
        msg = translate(
            template_email_text_expired,
            mapping=msg_mapping,
            target_language=language
        )

    subject = translate(
        template_subject,
        mapping={u"days": days_to_expire},
        target_language=language
    )

    api.portal.send_email(recipient=recipient,
                          subject=subject,
                          body=msg)


def days_since_event(event_date, current_date):
    """
    Returns the number of days difference
    between two given dates
    """
    # make both dates timezone aware
    if not event_date.tzinfo:
        event_date = pytz.utc.localize(event_date)
    if not current_date.tzinfo:
        current_date = pytz.utc.localize(current_date)

    difference = current_date - event_date
    return difference.days
