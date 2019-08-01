*** Settings ***

Resource  pwexpiryp52_keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${wrong_pw_email_error_msg} =  Login failed. Both email address and password are case sensitive, check that caps lock is not enabled. If you have entered your password correctly, your account might be locked. You can reset your password, or contact an administrator to unlock it, using the Contact form.
${wrong_pw_username_error_msg} =  Login failed. Both login name and password are case sensitive, check that caps lock is not enabled. If you have entered your password correctly, your account might be locked. You can reset your password, or contact an administrator to unlock it, using the Contact form.

*** Test cases ***

Test Username Error Message With Wrong Password
    Setup PWexpiry Use Username Login
    Log in  test_user_1  test_user_1
    Page Should Contain  You are now logged in
    Page Should Not Contain  ${wrong_pw_username_error_msg}
    Plone52 Log out

    Log in  test_user_1  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Log in  test_user_1  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Log in  test_user_1  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Log in  test_user_1  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Log in  test_user_1  test_user_1
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

Test Email Error Message With Wrong Password
    Setup PWexpiry Use Email Login
    Log in  test_user_1@none.com  test_user_1
    Page Should Contain  You are now logged in
    Page Should Not Contain  ${wrong_pw_email_error_msg}
    Plone52 Log out

    Log in  test_user_1@none.com  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Log in  test_user_1@none.com  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Log in  test_user_1@none.com  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Log in  test_user_1@none.com  wrong_pw
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Log in  test_user_1@none.com  test_user_1
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}
