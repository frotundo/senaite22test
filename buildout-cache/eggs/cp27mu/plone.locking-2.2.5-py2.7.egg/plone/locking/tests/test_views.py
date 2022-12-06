# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.locking.browser.locking import LockingInformation
from plone.locking.browser.locking import LockingInformationFallback
from plone.locking.testing import PLONE_LOCKING_INTEGRATION_TESTING
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest


class TestLockInfoViewWithoutLocking(unittest.TestCase):

    layer = PLONE_LOCKING_INTEGRATION_TESTING

    view = "@@plone_lock_info"

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]

        setRoles(self.portal, TEST_USER_ID, ["Manager", "Site Administrator"])

        self.portal.invokeFactory("News Item", id="news1", title="News Item 1")
        self.news = self.portal["news1"]

        # Remove plone.locking from Document content type
        fti = queryUtility(IDexterityFTI, name="Document")
        behavior_list = [a for a in fti.behaviors if a != "plone.locking"]
        fti.behaviors = tuple(behavior_list)

        self.portal.invokeFactory("Document", id="doc1", title="Document 1")
        self.doc = self.portal["doc1"]

    def test_browser_view_available_for_content_with_locking_behavior(self):
        content = self.news
        view = content.restrictedTraverse(self.view)
        self.assertIsInstance(view, LockingInformation)

    def test_browser_view_available_for_content_without_locking_behavior(self):
        content = self.doc
        view = content.restrictedTraverse(self.view)
        self.assertIsInstance(view, LockingInformationFallback)
