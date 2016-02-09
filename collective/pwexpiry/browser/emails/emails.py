from Products.Five import BrowserView


class NotificationEmail(BrowserView):

    def __call__(self, **kwargs):
        """
        """
        self.days = kwargs['days']
        return self.index(**kwargs)
    
    @property
    def has_expired(self):
        return self.days <= 0
