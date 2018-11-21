*** Settings ***

Resource  pwexpiryp4.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${wrong_pw_email_error_msg} =  Login failed. Both email address and password are case sensitive, check that caps lock is not enabled. If you have entered your password correctly, your account might be locked. You can reset your password, or contact an administrator to unlock it, using the Contact form.
${wrong_pw_username_error_msg} =  Login failed. Both login name and password are case sensitive, check that caps lock is not enabled. If you have entered your password correctly, your account might be locked. You can reset your password, or contact an administrator to unlock it, using the Contact form.

*** Test cases ***

Test Username Error Message With Wrong Password
    Setup PWexpiry Use Username Login
    Input Text  id=__ac_name  test_user_1
    Input Text  id=__ac_password  test_user_1
    Click Button  Log in
    Page Should Contain  You are now logged in
    Page Should Not Contain  ${wrong_pw_username_error_msg}
    Log out

    Input Text  id=__ac_name  test_user_1
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Input Text  id=__ac_name  test_user_1
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Input Text  id=__ac_name  test_user_1
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Input Text  id=__ac_name  test_user_1
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

    Input Text  id=__ac_name  test_user_1
    Input Text  id=__ac_password  test_user_1
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_username_error_msg}

Test Email Error Message With Wrong Password
    Setup PWexpiry Use Email Login
    Input Text  id=__ac_name  test_user_1@none.com
    Input Text  id=__ac_password  test_user_1
    Click Button  Log in
    Page Should Contain  You are now logged in
    Page Should Not Contain  ${wrong_pw_email_error_msg}
    Log out

    Input Text  id=__ac_name  test_user_1@none.com
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Input Text  id=__ac_name  test_user_1@none.com
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Input Text  id=__ac_name  test_user_1@none.com
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Input Text  id=__ac_name  test_user_1@none.com
    Input Text  id=__ac_password  wrong_pw
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}

    Input Text  id=__ac_name  test_user_1@none.com
    Input Text  id=__ac_password  test_user_1
    Click Button  Log in
    Page Should Not Contain  You are now logged in
    Page Should Contain  ${wrong_pw_email_error_msg}
