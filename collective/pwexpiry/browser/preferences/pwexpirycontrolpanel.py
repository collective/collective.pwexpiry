from itertools import chain

from DateTime import DateTime
from Acquisition import aq_inner
from collective.pwexpiry.config import DATETIME_FORMATSTRING
from zope.component import getMultiAdapter
from plone.app.controlpanel.usergroups import UsersOverviewControlPanel
from plone.protect import CheckAuthenticator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone import PloneMessageFactory as _

class PwExpiryControlPanel(UsersOverviewControlPanel):

    def __call__(self):

        form = self.request.form
        submitted = form.get('form.submitted', False)
        search = form.get('form.button.Search', None) is not None
        findAll = form.get('form.button.FindAll', None) is not None
        self.searchString = not findAll and form.get('searchstring', '') or ''
        self.searchResults = []
        self.newSearch = False

        if search or findAll:
            self.newSearch = True

        if submitted:
            if form.get('form.button.Modify', None) is not None:
                self.manageUser(form.get('users', None),)

        if not(self.many_users) or bool(self.searchString):
            self.searchResults = self.doSearch(self.searchString)
        return self.index()

    def doSearch(self, searchString):
        mtool = getToolByName(self, 'portal_membership')
        searchView = getMultiAdapter((aq_inner(self.context), self.request),
            name='pas_search')
        explicit_users = searchView.merge(chain(
                *[searchView.searchUsers(**{field: searchString}
            ) for field in ['login', 'fullname', 'email']]), 'userid')
        results = []
        for user_info in explicit_users:
            userId = user_info['id']
            user = mtool.getMemberById(userId)
            if user is None:
                continue
            user_info['password_date'] = \
                user.getProperty('password_date', '2000/01/01')
            user_info['last_notification_date'] = \
                user.getProperty('last_notification_date', '2000/01/01')
            user_info['fullname'] = user.getProperty('fullname', '')
            results.append(user_info)

        results.sort(key=lambda x: x is not None and x['fullname'] is not None and \
            normalizeString(x['fullname']) or '')
        return results

    def manageUser(self, users=None):
        if users is None:
            users = []
        CheckAuthenticator(self.request)

        if users:
            context = aq_inner(self.context)
            mtool = getToolByName(context, 'portal_membership')
            utils = getToolByName(context, 'plone_utils')

            for user in users:
                member = mtool.getMemberById(user.id)
                password_date = member.getProperty('password_date', '2000/01/01')
                new_password_date = DateTime(user.get('password'))
                if password_date != new_password_date:
                    member.setMemberProperties(
                        {'password_date': new_password_date}
                    )

                notification_date = member.getProperty(
                    'last_notification_date', '2000/01/01'
                )
                new_notification = DateTime(user.get('notification'))
                if notification_date != new_notification:
                    member.setMemberProperties(
                        {'last_notification_date': new_notification}
                    )

            utils.addPortalMessage(_(u'Changes applied.'))

    def formatDate(self, date):
        return date.strftime(DATETIME_FORMATSTRING)
