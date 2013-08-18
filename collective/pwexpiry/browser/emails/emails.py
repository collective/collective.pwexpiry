from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class NotificationEmail(BrowserView):

    def __call__(self, **kwargs):
        """
        """
        return self.index(**kwargs)