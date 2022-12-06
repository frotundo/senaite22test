# -*- coding: utf-8 -*-
# This directory is used in a test in dependency.txt.
# We need a package with a module that has no __file__ attribute.
# This can happen in corner cases, for example with 'backports' on Python 2.7.
# See https://github.com/zopefoundation/z3c.autoinclude/issues/6.
del __file__
