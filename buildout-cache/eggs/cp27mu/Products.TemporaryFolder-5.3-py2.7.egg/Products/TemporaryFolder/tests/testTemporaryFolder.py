##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################


import unittest


class TestSimpleTemporaryContainer(unittest.TestCase):

    def _makeOne(self, *args, **kw):
        from Products.TemporaryFolder.TemporaryFolder import \
            SimpleTemporaryContainer
        return SimpleTemporaryContainer(*args, **kw)

    def test_init(self):
        container = self._makeOne(id='mount')
        self.assertEqual(container.getId(), 'mount')


class TestMountedTemporaryFolder(unittest.TestCase):

    def _makeOne(self, *args, **kw):
        from Products.TemporaryFolder.TemporaryFolder import \
            MountedTemporaryFolder
        return MountedTemporaryFolder(*args, **kw)

    def test_init(self):
        container = self._makeOne(id='mount', title='Mountpoint')
        self.assertEqual(container.getId(), 'mount')
        self.assertEqual(container.title_or_id(), 'Mountpoint')
