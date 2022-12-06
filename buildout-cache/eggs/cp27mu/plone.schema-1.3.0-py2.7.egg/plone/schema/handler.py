from plone.supermodel.exportimport import BaseHandler
from zope.schema import URI
from plone.schema.email import Email
from plone.schema.jsonfield import JSONField

URIHandler = BaseHandler(URI)
EmailHandler = BaseHandler(Email)
JSONHandler = BaseHandler(JSONField)
