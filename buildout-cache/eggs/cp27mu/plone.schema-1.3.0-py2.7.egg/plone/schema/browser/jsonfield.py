from zope.component import adapter
from zope.interface import implementer
from z3c.form.interfaces import ITextAreaWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IWidget
from plone.app.z3cform.interfaces import IPloneFormLayer
from zope.component import adapts
from plone.schema.jsonfield import IJSONField

import json


class IJSONFieldWidget(ITextAreaWidget):
    """ JSON Widget """


@implementer(IJSONFieldWidget)
class JSONWidget(TextAreaWidget):
    klass = u'json-widget'
    value = None


@adapter(IJSONField, IPloneFormLayer)
@implementer(IFieldWidget)
def JSONFieldWidget(field, request):
    return FieldWidget(field, JSONWidget(request))


@implementer(IDataConverter)
class JSONDataConverter(object):
    """A JSON data converter."""

    adapts(IJSONField, IWidget)

    def __init__(self, field, widget):
        self.field = field
        self.widget = widget

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        return json.dumps(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""

        if value == u'':
            return self.field.missing_value

        return self.field.fromUnicode(value)
