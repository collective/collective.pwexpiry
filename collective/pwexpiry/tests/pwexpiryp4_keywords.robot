*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

*** Variables ***

${PORT} =  55001
${ZOPE_URL} =  http://localhost:${PORT}
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

Setup PWexpiry Use Username Login
    Start Browser and Log In as Site Owner
    Go to Security Settings
    Select Checkbox  id=form.enable_user_pwd_choice
    Click Button  id=form.actions.save
    Go to Configuration Registry
    Input Text  id=q  validity_period
    Click Button  Filter
    Click Link  collective pwexpiry validity_period
    Wait Until Element Is Visible  id=form-widgets-value
    Input Text  id=form-widgets-value  0
    Click Button  id=form-buttons-save
    Go to Users and Groups
    Click Button  name=form.button.AddUser
    Input Text  id=form.fullname  Test User 1
    Input Text  id=form.username  test_user_1
    Input Text  id=form.email  test_user_1@none.com
    Input Text  id=form.password  test_user_1
    Input Text  id=form.password_ctl  test_user_1
    Click Button  id=form.actions.register
    Log out

Setup PWexpiry Use Email Login
    Start Browser and Log In as Site Owner
    Go to Security Settings
    Select Checkbox  id=form.enable_user_pwd_choice
    Select Checkbox  id=form.use_email_as_login
    Click Button  id=form.actions.save
    Go to Configuration Registry
    Input Text  id=q  validity_period
    Click Button  Filter
    Click Link  collective pwexpiry validity_period
    Wait Until Element Is Visible  id=form-widgets-value
    Input Text  id=form-widgets-value  0
    Click Button  id=form-buttons-save
    Go to Users and Groups
    Click Button  name=form.button.AddUser
    Input Text  id=form.fullname  Test User 1
    Input Text  id=form.email  test_user_1@none.com
    Input Text  id=form.password  test_user_1
    Input Text  id=form.password_ctl  test_user_1
    Click Button  id=form.actions.register
    Log out

