collective.pwexpiry
===================

Introduction
============

The ``collective.pwexpiry`` package is an add-on Product for Plone that brings the
feature of controlling the password expiration in Plone. It is useful when there's
a need of forcing the portal's members to follow the specific password policy.

Features
========
* Possibility to register and define custom password validation methods
* Possibility to define user's passwords period of validity
* Possibility to check if the password has been used in the last x variants. And disallow
  reuse.
* Possibility to register custom notification actions to be triggered when the password's
  period of validity is getting closer
* Provides a script that can be periodically executed from the command line (i.e. by cron).
  The script checks for the user's passwords expiration dates and triggers the registered
  notification actions (i.e. sending email to the relevant users).
* Provides a protection mechanizm to avoid notifying given user twice the same day
* Possibility to lock an account if too many invalid password attemps were tried

Installation
============

1. Add collective.pwexpiry to your plone.recipe.zope2instance section's eggs::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    eggs =
        ...
        collective.pwexpiry

2. Install the Product via portal_quickinstaller.

Configuration and customization
===============================

Password period of validity
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The password's period of validity is set in the configuration registry tool, and have
a default value of 90 days. It can be easily customized by creating a registry.xml file
in your custom pakage's gereric setup profile containing the configuration code::

    <registry>
        <record name="collective.pwexpiry.validity_period">
            <value>360</value>
        </record>
    </registry>

To disable password expiration, set `validity_period` to `0`.

Last X Passwords check
~~~~~~~~~~~~~~~~~~~~~~

It's possible to check if the new password has already been used (a history of the last `password_history_size` password hashes is kept).

`password_history_size` defaults to 0, which means: there is no active check for re-used passwords.

You need to manualy activate that feature with a registry record in registry.xml::

    <registry>
        <record name="collective.pwexpiry.password_history_size">
            <value>10</value>
        </record>
    </registry>


Defining notification actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default - there is a notification action defined that sends the notification email
to the user when his password period of validity is going to end in 15 days.
But there is a possibility to register a custom methods that would be triggered
according to their implementation.

To register your own notification action you need to::
 1. Register adapter providing ``IExpirationCheck`` interface::

     <configure xmlns="http://namespaces.zope.org/zope">
       <adapter
         name="last_few_days_before_expiration"
         factory=".actions.LastFewDaysBeforeExpiration"
         provides="collective.pwexpiry.interfaces.IExpirationCheck"
         for="zope.interface.Interface"
         />
     </configure>

 2. Implement the adapter's ``__call__`` and ``notification_action`` methods::

      class LastFewDaysBeforeExpiration(object):
          implements(IExpirationCheck)

          # Trigger on number of days before password expiration
          notify_on = (7, 4, 3, 2, 1)

          def __init__(self, context):
              self.context = context

          def __call__(self, days_to_expire):
              """
              Returns True whe n the notification_action
              method have to be executed
              """
              try:
                  notify_on = iter(self.notify_on)
              except TypeError:
                  notify_on = (self.notify_on,)

              if days_to_expire in notify_on:
                  return True
              else:
                  return False

          def notification_action(self, userdata, days_to_expire):
              """
              Implementation of the notification action.
              In this case it's sendin an email notification
              """
              send_notification_email(userdata, days_to_expire)


Defining custom password validation methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package allows to define your own password valdation methods
executed when the user set his initial password on registration or
changing his actual password by in the change password form or throught
the password reset mechanizm.

To register your own notification action you need to::

 1. Register adapter providing ``ICustomPasswordValidator`` interface::

     <configure xmlns="http://namespaces.zope.org/zope">
       <adapter
         name="my_password_policy"
         factory=".password_validators.MyPasswordValidator"
         provides="collective.pwexpiry.interfaces.ICustomPasswordValidator"
         for="zope.interface.Interface"
         />
     </configure>

 2. Implement the adapter's ``__call__`` and ``notification_action`` methods::

      class MyPasswordValidator(object):
          implements(ICustomPasswordValidator)

          def __init__(self, context):
              self.context = context

          def validate(self, password, data):
              if len(password) < 8:
                  return _(u'Passwords must be at least 8 characters in length.')

Executing the notification script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The notification script should be executed **once a day** to check the user's passwords
expiration dates and trigger relevant notification actions.

Here's an example of how the script can be executed from the command line::

    $ cd ${buildoout:directory}
    $ ./bin/instance run src/collective.pwexpiry/collective/pwexpiry/scripts/notify_and_expire.py ${your-plonesite-id}


Locking out accounts if an invalid password is entered too many times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the package is installed, a new PAS plugin is included, which will count invalid password attempts when logging in.
If the number of invalid attempts is higher than a configurable threshold, the account will be locked out for a certain amount of hours.
If the account hasn't been locked yet, entering the password correctly will reset this counter to zero.
An account can be re-activated by an administrator changing its password.


Controlling the additional user's properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``collective.pwexpiry`` package creates new user's properties:
 * ``password_date`` - the date when the user has changed his passoword
 * ``last_notification_date`` - the date when the last notification action has been performed for the user
 * ``account_locked_date`` - the date when the account was locked
 * ``account_locked`` - boolean telling if the account was locked or not
 * ``password_tries`` - the number of incorrect password attempts

In order to be able to control manually the new user's properties manually - there's a
control panel form available under url: ``/@@pwexpiry-controlpanel``.


Setting how many tries before locking the account and for how much time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is managed with values in the registry:

 * ``collective.pwexpiry.allowed_tries`` - Allows you to choose how many attempts are allowed
 * ``collective.pwexpiry.disable_time`` - Allows you to specify for how many hours the user should be locked out


TODO
====

Write tests!
~~~~~~~~~~~~

Author & Contact
================

:Author:
 * Radosław Jankiewicz ``radoslaw.jankiewicz@stxnext.pl``

License
=======

This package is licensed under the Zope Public License.

.. _`Plone 4.2`: http://pypi.python.org/pypi/Plone/4.2
