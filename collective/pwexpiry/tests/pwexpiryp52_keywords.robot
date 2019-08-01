*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

*** Variables ***

${ZOPE_URL} =  http://${ZOPE_HOST}:${ZOPE_PORT}
${PLONE_URL} =  ${ZOPE_URL}/plone
${BROWSER} =  Firefox

*** Keywords ***

Start Browser and Autologin as
    [arguments]  ${role}

    Open Test Browser
    Enable Autologin as  $role

Start Browser and Log In as Site Owner
    Open Test Browser
    Log In As Site Owner
    Click Link  link=Home

Go to Site Setup
    Go to   ${PLONE_URL}/@@overview-controlpanel
    Wait until location is  ${PLONE_URL}/@@overview-controlpanel

Go to Security Settings
    Go to   ${PLONE_URL}/@@security-controlpanel
    Wait until location is  ${PLONE_URL}/@@security-controlpanel

Go to Users and Groups
    Go to   ${PLONE_URL}/@@usergroup-userprefs
    Wait until location is  ${PLONE_URL}/@@usergroup-userprefs

Go to Configuration Registry
    Go to   ${PLONE_URL}/portal_registry
    Wait until location is  ${PLONE_URL}/portal_registry

Plone52 Log out
    Go to  ${PLONE_URL}/logout
    Page Should Contain  You are now logged out.

Setup PWexpiry Use Username Login
    Start Browser and Log In as Site Owner
    Go to Users and Groups
    Click Button  id=add-new-user
    Wait Until Element Is Not Visible  css:div#plone-loader
    Input Text  id=form-widgets-fullname  Test User 1
    Input Text  id=form-widgets-email  test_user_1@none.com
    Input Text  id=form-widgets-username  test_user_1
    Input Text  id=form-widgets-password  test_user_1
    Input Text  id=form-widgets-password_ctl  test_user_1
    Press Key  id=form-widgets-password_ctl  \\13
    Wait Until Element Is Not Visible  css:div#plone-loader
    Plone52 Log out

Setup PWexpiry Use Email Login
    Start Browser and Log In as Site Owner
    Go to Security Settings
    Select Checkbox  id=form-widgets-use_email_as_login-0
    Click Button  id=form-buttons-save
    Go to Users and Groups
    Click Button  id=add-new-user
    Wait Until Element Is Not Visible  css:div#plone-loader
    Input Text  id=form-widgets-fullname  Test User 1
    Input Text  id=form-widgets-email  test_user_1@none.com
    Input Text  id=form-widgets-password  test_user_1
    Input Text  id=form-widgets-password_ctl  test_user_1
    Press Key  id=form-widgets-password_ctl  \\13
    Wait Until Element Is Not Visible  css:div#plone-loader
    Plone52 Log out

