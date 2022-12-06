""" Tests
"""
import re
import six
import unittest
import doctest

class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", want)
            got = re.sub(' encoding="utf-8"', '', want)
            # want = re.sub("b'(.*?)'", "'\\1'", want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(
            'plone.schema.jsonfield',
            checker=Py23DocChecker()
        ),
    ))
