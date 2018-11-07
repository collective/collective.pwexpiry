Changelog
=========

1.0.0 (unreleased)
------------------

- Restore compatibility with Plone 4.3.
  [hvelarde]

- Add uninstall profile and tests.
  [hvelarde]


0.12.0 (2018-05-30)
-------------------

- Update german translations
  [fRiSi]

- Refactor the notify_and_expire script so it can be added as a zopectl command
  [frapell]

- Use SERVER_URL and SERVER_NAME for including additional info in emails
  [frapell]


0.11.3 (2017-12-06)
-------------------

- Password validation does not raise UnicodeDecodeError if password
  contains non-ascii characters [fRiSi]


0.11.2 (2017-07-31)
-------------------

- Include upgrade step for the whitelist feature
  [frapell]


0.11.1 (2017-07-31)
-------------------

- Re-release
  [frapell]


0.11 (2017-07-31)
-----------------

- Include the ability to whitelist userids so they would not expire nor be locked
  [frapell]


0.10 (2017-02-21)
-----------------

- Product now works on Plone 5
  [enfold-josh]

- Javascript for login popup is only needed for Plone 4
  [frapell]


0.9.1 (2016-05-23)
------------------

- fix rst2html for pypi page [fRiSi]


0.9 (2016-05-23)
----------------

- Change the E-Mail Template to use a customizeable view.
  [pcdummy]

- Fix an encoding problem with usernames in notify_and_expire.
  [pcdummy]

- Fix javascripts with Plone 4.3.8, theres no more "ieversion()" function.
  [pcdummy]

- Fix translations for "password disabled" statusmessage
  (this fixes #11)
  [fRiSi]

- Update german translations.
  [pcdummy]

- Change the notification e-mail to a translated text e-mail.
  [pcdummy]

- Show status message "your account has expired" in login popup.
  [pcdummy]

- Update german translations.
  [pcdummy]

- Do not exipre passwords if `validity_period` is set to 0
  [fRiSi]

- Add password history check (not in last x passwords).
  [pcdummy]

- Enable the example_validator only when there is a browserlayer.
  [pcdummy]

- Add a skins layer and remove the confusing > 5 chars message from
  pwreset_form.
  [pcdummy]

- Update german translations and translate example_validator.
  [pcdummy]


0.8.1 (2015-05-06)
------------------

- Template typo
  [frapell]

- Update italian translation
  [giacomos]


0.8 (2015-04-20)
----------------

- Update translations
  [frapell]

- Improve control panel tool to allow admins to unlock accounts
  [frapell]


0.7 (2015-03-25)
----------------

- Ignore Managers from password expiring
  [frapell]

- Bugfix: If a wrong password was entered that goes over the limit, do not
  add a response header. Only do it when entering correctly
  [frapell]

- When comparing dates, make sure both are timezone aware
  [frapell]

- Ignore case when checking for name and username in password.
  [enfold-josh]

- Change script to accept a path and use traversal to get plone site since it
  may not always be in the application root.
  [enfold-josh]

- Redirect to $portal_url/mail_password_form instead of just /mail_password_form
  [enfold-josh]

- Alter notification email to support days <= 0.
  [enfold-josh]


0.6 (2015-03-13)
----------------

- Use a friendlier date format for the control panel
  [frapell]


0.5 (2014-11-28)
----------------

- Add i18n and italian translation
  [giacomos]

- No need to include 'control panel' in the control panel title
  [frapell]


0.4 (2014-09-11)
----------------

- Add member properties, registry keys, events subscribers, and a PAS plugin
  to allow blocking a user if he enters too many incorrect passwords.
  [frapell]

- Patch ZODBUserManager.authenticateCredentials so it fires events when entering
  valid or invalid credentials.
  [frapell]

- Patch CMFPlone/RegistrationTool instead of CMFDefault/RegistrationTool.
  [frapell]


0.3 (2014-09-10)
----------------

- Properly package
  [frapell]


0.2 (2013-08-18)
----------------

- correct pypi classifiers

- initial code
