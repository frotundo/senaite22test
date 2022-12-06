##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Simple :class:`zope.security.interfaces.ISecurityPolicy` implementations.

As a reminder, ``ISecurityPolicy`` objects are factories for producing
:class:`zope.security.interfaces.IInteraction` objects. That means
that the classes themselves are implementations of
``ISecurityPolicy``.
"""
import zope.interface

from zope.security.checker import CheckerPublic
from zope.security.interfaces import IInteraction
from zope.security.interfaces import ISecurityPolicy
from zope.security._definitions import system_user


@zope.interface.implementer(IInteraction)
@zope.interface.provider(ISecurityPolicy)
class ParanoidSecurityPolicy(object):
    """
    Prohibit all access by any non-system principal, unless the item
    is :data:`public <zope.security.checker.CheckerPublic>`.

    This means that if there are no participations (and hence no
    principals), then access is allowed.
    """

    def __init__(self, *participations):
        self.participations = []
        for participation in participations:
            self.add(participation)

    def add(self, participation):
        if participation.interaction is not None:
            raise ValueError("%r already belongs to an interaction"
                             % participation)
        participation.interaction = self
        self.participations.append(participation)

    def remove(self, participation):
        if participation.interaction is not self:
            raise ValueError("%r does not belong to this interaction"
                             % participation)
        self.participations.remove(participation)
        participation.interaction = None

    def checkPermission(self, permission, object):
        if permission is CheckerPublic:
            return True

        users = [p.principal
                 for p in self.participations
                 if p.principal is not system_user]

        return not users


@zope.interface.provider(ISecurityPolicy)
class PermissiveSecurityPolicy(ParanoidSecurityPolicy):
    """
    Allow all access.
    """

    def checkPermission(self, permission, object):
        return True
