===============
 ``zope.copy``
===============

.. image:: https://img.shields.io/pypi/v/zope.copy.svg
        :target: https://pypi.python.org/pypi/zope.copy/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.copy.svg
        :target: https://pypi.org/project/zope.copy/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.copy.svg?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.copy

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.copy/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.copy?branch=master

.. image:: https://readthedocs.org/projects/zopecopy/badge/?version=latest
        :target: http://zopecopy.readthedocs.org/en/latest/
        :alt: Documentation Status

This package provides a pluggable mechanism for copying persistent objects.

Documentation is hosted at https://zopecopy.readthedocs.io/en/latest/


=========
 Changes
=========

4.2 (2018-10-04)
================

- Use the latest and fastest protocol when pickling and unpickling and object
  during the clone operation

- Add support for Python 3.7.


4.1.0 (2017-07-31)
==================

- Drop support for Python 2.6, 3.2 and 3.3.

- Add support for Python 3.5 and 3.6.

- Restore ``zope.component`` as a testing requirement for running doctests.

4.0.3 (2014-12-26)
==================

- Add support for PyPy3.

4.0.2 (2014-03-19)
==================

- Add support for Python 3.3 and 3.4.

- Update ``boostrap.py`` to version 2.2.

4.0.1 (2012-12-31)
==================

- Flesh out PyPI Trove classifiers.

4.0.0 (2012-06-13)
==================

- Add support for Python 3.2.

- Drop ``zope.component`` as a testing requirement. Instead, register
  explicit (dummy) adapter hooks where needed.

- Add PyPy support.

- 100% unit test coverage.

- Add support for continuous integration using ``tox`` and ``jenkins``.

- Add Sphinx documentation:  moved doctest examples to API reference.

- Add 'setup.py docs' alias (installs ``Sphinx`` and dependencies).

- Add 'setup.py dev' alias (runs ``setup.py develop`` plus installs
  ``nose``, ``coverage``, and testing dependencies).

- Drop support for Python 2.4 and 2.5.

- Include tests of the LocationCopyHook from zope.location.

3.5.0 (2009-02-09)
==================

- Initial release. The functionality was extracted from ``zc.copy`` to
  provide a generic object copying mechanism with minimal dependencies.


