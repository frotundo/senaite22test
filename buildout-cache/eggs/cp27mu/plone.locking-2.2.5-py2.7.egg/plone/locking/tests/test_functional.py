# -*- coding: utf-8 -*-
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.locking.testing import PLONE_LOCKING_FUNCTIONAL_TESTING
from plone.locking.testing import optionflags
from plone.testing import layered
from Products.CMFCore.utils import getToolByName

import doctest
import unittest


def setup(doctest):
    portal = doctest.globs['layer']['portal']
    portal_membership = getToolByName(portal, 'portal_membership')
    portal_membership.addMember('member1', 'secret', ('Member', ), [])
    portal_membership.addMember('member2', 'secret', ('Member', ), [])

    logout()
    login(portal, 'member1')
    setRoles(portal, 'member1', ['Manager', ])
    portal.invokeFactory('Document', 'doc')
    setRoles(portal, 'member1', ['Member', ])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(
        layered(
            doctest.DocFileSuite(
                'tests/locking.rst',
                package='plone.locking',
                optionflags=optionflags,
                setUp=setup,
            ),
            layer=PLONE_LOCKING_FUNCTIONAL_TESTING,
        )
    )
    return suite
