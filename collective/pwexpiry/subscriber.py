# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from collective.pwexpiry.logger import logger
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility


def ValidPasswordEntered(user, event):

    registry = queryUtility(IRegistry)
    if not registry:
        return

    # Now check if this user had his account locked
    if user.getProperty('account_locked', False):
        # It was locked, check how much time ago
        locked_date = user.getProperty('account_locked_date')
        disable_time = registry['collective.pwexpiry.disable_time']

        portal = api.portal.get()
        current_time = portal.ZopeTime()
        delta = current_time.asdatetime() - locked_date.asdatetime()
        # We are checking in hours, so we divide in 3600 the elapsed seconds
        if (delta.seconds / 3600) >= disable_time:
            # Enough time has elapsed
            user.setMemberProperties({'account_locked': False,
                                      'password_tries': 0})
            msg = 'User {0} logged in after lock time; account is now unlocked'
            logger.info(msg.format(user))
        else:
            user_disabled_time = disable_time - (delta.seconds / 3600)
            user.REQUEST.RESPONSE.setHeader('user_disabled', user.getId())
            user.REQUEST.RESPONSE.setHeader('user_disabled_time', user_disabled_time)
            msg = 'User {0} tried to log in but account is locked for {1} hours'
            logger.warn(msg.format(user, user_disabled_time))
            raise Unauthorized

    else:
        # This account has not been locked, reset current_tries counter
        if user.getProperty('password_tries', 0) > 0:
            user.setMemberProperties({'password_tries': 0})


def InvalidPasswordEntered(user, event):

    # If we are here, means that the provided credentials were invalid

    # If user is Manager, then ignore this and do not block
    if user.has_role('Manager'):
        return

    registry = queryUtility(IRegistry)
    if not registry:
        return

    whitelisted = registry.get('collective.pwexpiry.whitelisted_users')
    if whitelisted and user.getId() in whitelisted:
        return

    allowed_tries = registry['collective.pwexpiry.allowed_tries']
    current_tries = user.getProperty('password_tries', 0)

    # Add +1 to the current tries, and lock the account if it went over the
    # limit allowed
    current_tries += 1
    user.setMemberProperties({'password_tries': current_tries})
    if current_tries >= allowed_tries:
        portal = api.portal.get()
        current_time = portal.ZopeTime()
        user.setMemberProperties({'account_locked_date': current_time,
                                  'account_locked': True})
        msg = 'User {0} has tried to access {1} times with an invalid password; account is locked'  # noqa: E501
        logger.warn(msg.format(user, current_tries))
