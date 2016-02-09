from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_password_date(self):
        return self.context.getProperty('password_date', '')

    def set_password_date(self, value):
        return self.context.setMemberProperties({'password_date': value})
    password_date = property(get_password_date, set_password_date)

    def get_last_notification_date(self):
        return self.context.getProperty('last_notification_date', '')

    def set_last_notification_date(self, value):
        return self.context.setMemberProperties(
            {'last_notification_date': value}
        )
    last_notification_date = property(get_last_notification_date,
                                      set_last_notification_date)
