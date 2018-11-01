# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    @property
    def password_date(self):
        return self.context.getProperty('password_date', '')

    @password_date.setter
    def password_date(self, value):
        return self.context.setMemberProperties({'password_date': value})

    @property
    def last_notification_date(self):
        return self.context.getProperty('last_notification_date', '')

    @last_notification_date.setter
    def last_notification_date(self, value):
        return self.context.setMemberProperties({'last_notification_date': value})  # noqa: E501
