#
import argparse
import logging
import os
import sys
import transaction

from DateTime import DateTime
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.User import system
from collective.pwexpiry.interfaces import IExpirationCheck
from collective.pwexpiry.utils import days_since_event
from plone import api
from plone.registry.interfaces import IRegistry
from Testing.makerequest import makerequest
from zope.component import getAdapters, getUtility
from zope.component.hooks import setSite
from zope.globalrequest import setRequest


def notify_and_expire():
    """
    For each registered user check all the conditions and execute
    the notification action
    """
    logger = logging.getLogger("collective.pwexpiry")
    logger.info("*" * 8 + "Executing notify_an_expire script" + "*" * 8)

    portal = api.portal.get()
    registry = getUtility(IRegistry)
    validity_period = registry["collective.pwexpiry.validity_period"]

    if validity_period == 0:
        # do not do any notifications, if password expiration has been disabled
        return

    notifications_to_use = set()
    if "collective.pwexpiry.notification_actions" in registry:
        notifications_to_use = registry[
            "collective.pwexpiry.notification_actions"
        ]
    current_time = portal.ZopeTime()
    local_tz = current_time.timezone()

    whitelisted = registry.get("collective.pwexpiry.whitelisted_users")
    for user_id in portal.acl_users.source_users.getUserIds():
        # Ignore whitelisted
        if whitelisted and user_id in whitelisted:
            continue

        user = portal.portal_membership.getMemberById(user_id)
        password_date = DateTime(
            user.getProperty("password_date", "2000/01/01")
        )
        last_notification_date = DateTime(
            user.getProperty("last_notification_date", "2000/01/01")
        )
        last_notification_date = last_notification_date.toZone(local_tz)

        if password_date == DateTime("2000/01/01"):
            # The user has not set the changed the password yet -
            # the current time is set as the initial value
            user.setMemberProperties({"password_date": current_time})
            logger.info("Set new password reset date for user: %s" % user_id)
            continue

        # Counting days difference since the user reset his password
        since_last_pw_reset = days_since_event(
            password_date.asdatetime(), current_time.asdatetime()
        )
        # Counting days diff since the notification has been sent to the user
        since_last_notification = days_since_event(
            last_notification_date.asdatetime(), current_time.asdatetime()
        )
        # Number of days before the user's password expires
        days_to_expire = validity_period - since_last_pw_reset

        # Search for registered notifications and execute them
        notifications = getAdapters((portal,), IExpirationCheck)
        for notification_name, notification in notifications:
            if (
                notifications_to_use
                and notification_name not in notifications_to_use
            ):
                msg = (
                    "Skipping notification %s because it is not in "
                    "registry['collective.pwexpiry.notification_actions']"
                )
                logger.debug(msg % notification_name)
                continue
            if notification(days_to_expire):
                try:
                    # Protection of sending the
                    # expired notification email twice
                    pwres_to_notif = days_since_event(
                        password_date.asdatetime(),
                        last_notification_date.asdatetime(),
                    )
                    if pwres_to_notif > validity_period:
                        logger.warning(
                            "Omitting notification for user: '%s' "
                            "because the expiration email has already "
                            "been sent once." % (user_id)
                        )
                        break
                    # Protection of sending the notification email twice
                    if since_last_notification < 1:
                        logger.warning(
                            "Omitting notification for user: '%s' "
                            "because the notification has been already "
                            "sent today." % (user_id)
                        )
                        break

                    # Executing the notification
                    # action and updating user's property
                    notification.notification_action(user, days_to_expire)
                    logger.info(
                        "Triggered %s action for user: %s"
                        % (notification_name, user_id)
                    )
                    user.setMemberProperties(
                        {"last_notification_date": current_time}
                    )
                except Exception:
                    # Continue with the script even in case of problems
                    logger.exception(
                        "Error while performing notification: %s "
                        "for user: %s" % (notification_name, user_id)
                    )
                    continue


def entrypoint(app, args):
    # Logging configuration
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file")
    parser.add_argument("portal_path")
    args = parser.parse_args(args[2:])
    logger = logging.getLogger("collective.pwexpiry")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(args.log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    app = makerequest(app)
    newSecurityManager(None, system)

    # Set site
    try:
        site = app.restrictedTraverse(args.portal_path)
    except Exception:
        raise ValueError(
            "Wrong portal_path parameter; Please specify an existing "
            "site's path."
        )

    setSite(site=site)
    site.REQUEST["PARENTS"] = [site]
    site.REQUEST.setVirtualRoot("/")

    if os.getenv("SERVER_NAME"):
        site.REQUEST["SERVER_NAME"] = os.getenv("SERVER_NAME")
    if os.getenv("SERVER_URL"):
        site.REQUEST["SERVER_URL"] = os.getenv("SERVER_URL")

    setRequest(site.REQUEST)
    notify_and_expire()
    # commit transaction
    transaction.commit()
    app._p_jar.sync()


if __name__ == "__main__":
    app = globals()["app"]  # for pep8
    entrypoint(app, sys.argv[1:])
