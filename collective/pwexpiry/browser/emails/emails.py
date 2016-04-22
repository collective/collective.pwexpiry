# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from collective.pwexpiry.config import _
from zope.i18n import translate


class NotificationEmail(BrowserView):

    def __call__(self, **kwargs):
        """ A E-Mail Template,
        call this like this:

        email_template = getMultiAdapter(
            (api.portal.get(), request), name=notification_email
        )

        body = email_template(**{
            'username': safe_unicode(user.getProperty('fullname')),
            'days': days_to_expire,
            'language': language_code,
        })
        """
        language = kwargs['language']

        msg_mapping = {
            'username': kwargs['username'],
            'days': kwargs['days'],
        }
        if kwargs['days'] > 0:
            msg = translate(
                _('email_text',
                  default=u"""Hello ${username},

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
                  default=u"""Hello ${username},

Your password has expired.

Please ensure to reset your password before it's expired.
""",
                  mapping=msg_mapping,
                  ),
                target_language=language
            )

        return msg
