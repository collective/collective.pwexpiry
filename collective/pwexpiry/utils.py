from email.mime.text import MIMEText

import pytz
from collective.pwexpiry.config import _
from plone import api
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.publisher.browser import TestRequest


def send_notification_email(user, days_to_expire,
                            email_view='notification_email'):
    """
    """
    request = TestRequest()
    recipient = user.getProperty('email')
    subject = _('${days} days left to password expiration',
                mapping={u"days": days_to_expire})

    subject = translate(subject)
    email_template = getMultiAdapter(
        (api.portal.get(), request), name=email_view
    )
    body = email_template(**{'username': user.getProperty('fullname'),
                             'days': days_to_expire})
    api.portal.send_email(recipient=recipient,
                          subject=subject,
                          body=MIMEText(body, 'html'))


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
