This is fork of https://github.com/PierreQuentel/PyDbLite

It does support Python 3.11 and latest pip



PyDbLite
=============

PyDbLite is

* a fast, pure-Python, untyped, in-memory database engine, using
  Python syntax to manage data, instead of SQL
* a pythonic interface to SQLite using the same syntax as the
  pure-Python engine for most operations (except database connection
  and table creation because of each database specificities)

PyDbLite is suitable for a small set of data where a fully fledged DB would be overkill.

Supported Python versions: 3.9+

Build status: |build-status|

Latest Pypi release: |pypi|

Read the documentation: |docs|

Installation
---------------

PIP
~~~~~~~~~

.. code-block:: bash

    pip install pydblite

Manually
~~~~~~~~~

Download the source and execute

.. code-block:: bash

    python setup.py install

Changelog
---------------
`docs/source/changelog.rst <docs/source/changelog.rst>`_

Tests
---------------

Run tests with

.. code-block:: bash

    python -m unittest -v tests

Run individual tests like this:

.. code-block:: bash

    python -m unittest -v tests.test_pydblite.PyDbLiteTestCase
    python -m unittest -v tests.test_pydblite_sqlite.SQLiteTestCase
    python -m unittest -v tests.test_pydblite_sqlite.SQLiteTestCase.test_filter_or

The tests will not pass for Python 3.0-3.2 due to the unicode literal being invalid syntax

Run tests for python 2.7 and 3.4, pep8 verification and documentation with

.. code-block:: bash

    tox

Authors:
  * Pierre Quentel (pierre.quentel@gmail.com)
  * Bendik Rønning Opstad (bro.devel@gmail.com)
