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


class TestMountPoint(unittest.TestCase):

    def _makeOne(self, *args, **kw):
        from Products.TemporaryFolder.mount import MountPoint
        return MountPoint(*args, **kw)

    def test_init(self):
        mount = self._makeOne('/')
        self.assertEqual(mount._path, '/')
