# -*- coding: utf-8 -*-
import pytz
from collective.pwexpiry.config import _
from plone import api
from zope.i18n import translate


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
            _('email_text',
              default="""Hello ${username},

There are ${days} days left before your password expires!

Please ensure to reset your password before it's expired.
""",
              mapping=msg_mapping,
            ),
            target_language=language
        )
    else:
        msg = translate(
            _('email_text_expired',
              default="""Hello ${username},

Your password has expired.

Please ensure to reset your password before it's expired.
""",
              mapping=msg_mapping,
            ),
            target_language=language
        )

    subject = translate(
        _('email_subject',
          default=u"${days} days left to password expiration",
          mapping={'days': days_to_expire},
          ),
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
