# -*- coding: utf-8 -*-
from plone import api
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.pwexpiry")

PROJECTNAME = 'collective.pwexpiry'

# Ideally, this should be language dependent, but we'll do US default for now
DATETIME_FORMATSTRING = "%m/%d/%Y %H:%M"

IS_PLONE_5 = api.env.plone_version().startswith('5')
