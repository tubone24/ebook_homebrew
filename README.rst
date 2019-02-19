.. image:: https://raw.githubusercontent.com/tubone24/ebook_homebrew/master/doc_src/bookicon.png
   :target: https://ebook-homebrew.readthedocs.io/en/latest/
   :align: center
   :alt: ebook_homebrew

==============
Ebook_homebrew
==============

The ``Ebook_homebrew`` is changing file name to only digit name like ``001.jpg`` and make e-book format files.

------

.. image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/tubone24/ebook_homebrew/blob/master/LICENSE

.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
   :target: http://makeapullrequest.com

.. image:: https://travis-ci.org/tubone24/ebook_homebrew.svg?branch=master
   :target: https://travis-ci.org/tubone24/ebook_homebrew

.. image:: https://codecov.io/gh/tubone24/ebook_homebrew/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tubone24/ebook_homebrew

.. image:: https://api.codeclimate.com/v1/badges/a3e2d70a87998a18e225/maintainability
   :target: https://codeclimate.com/github/tubone24/ebook_homebrew/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/a3e2d70a87998a18e225/test_coverage
   :target: https://codeclimate.com/github/tubone24/ebook_homebrew/test_coverage
   :alt: Test Coverage

.. image:: https://img.shields.io/codeclimate/tech-debt/tubone24/ebook_homebrew.svg?style=flat
   :target: https://codeclimate.com/github/tubone24/ebook_homebrew/maintainability

.. image:: https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/?branch=master

.. image:: https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/badges/code-intelligence.svg?b=master
   :target: https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/?branch=master

.. image:: https://ci.appveyor.com/api/projects/status/mx93pu69tqkngjxv?svg=true
   :target: https://ci.appveyor.com/project/tubone24/ebook-homebrew

.. image:: https://img.shields.io/appveyor/tests/tubone24/ebook-homebrew.svg?style=flat
   :target: https://ci.appveyor.com/project/tubone24/ebook-homebrew

.. image:: https://dev.azure.com/meitantei-conan/ebook_homebrew/_apis/build/status/tubone24.ebook_homebrew?branchName=master
   :target: https://dev.azure.com/meitantei-conan/ebook_homebrew/_build?definitionId=1

.. image:: https://img.shields.io/azure-devops/tests/meitantei-conan/ebook_homebrew/1.svg?compact_message&style=flat
   :target: https://dev.azure.com/meitantei-conan/ebook_homebrew/_build?definitionId=1

.. image:: https://api.shippable.com/projects/5c64353c33944406008b4ae8/badge?branch=master
   :target: https://app.shippable.com/github/tubone24/ebook_homebrew/dashboard

.. image:: https://circleci.com/gh/tubone24/ebook_homebrew.svg?style=svg
   :target: https://circleci.com/gh/tubone24/ebook_homebrew

.. image:: https://img.shields.io/lgtm/alerts/g/tubone24/ebook_homebrew.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/tubone24/ebook_homebrew/alerts

.. image:: https://img.shields.io/lgtm/grade/python/g/tubone24/ebook_homebrew.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/tubone24/ebook_homebrew/context:python

.. image:: https://snyk.io/test/github/tubone24/ebook_homebrew/badge.svg?targetFile=requirements.txt
   :target: https://snyk.io/test/github/tubone24/ebook_homebrew?targetFile=requirements.txt

.. image:: https://readthedocs.org/projects/ebook-homebrew/badge/?version=latest
   :target: https://ebook-homebrew.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

.. image:: https://img.shields.io/pypi/dm/ebook-homebrew.svg
   :target: https://pypi.org/project/ebook-homebrew/#files

.. image:: https://img.shields.io/pypi/v/ebook-homebrew.svg
   :target: https://pypi.org/project/ebook-homebrew/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/ebook-homebrew.svg
   :target: https://pypi.org/project/ebook-homebrew/

.. image:: https://img.shields.io/pypi/format/ebook-homebrew.svg
   :target: https://pypi.org/project/ebook-homebrew/

.. image:: https://img.shields.io/gitter/room/tubone24/ebook_homebrew.svg
   :target: https://gitter.im/ebook_homebrew/community#

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/tubone24

.. image:: https://beerpay.io/tubone24/ebook_homebrew/badge.svg
   :target: https://beerpay.io/tubone24/ebook_homebrew

.. image:: https://badge.waffle.io/tubone24/ebook_homebrew.svg?columns=all
   :target: https://waffle.io/tubone24/ebook_homebrew
   :alt: Waffle.io - Columns and their card count

ebook_homebrew is command line interface which change file name to only digit name like 001.jpg and make e-book format files.

Getting Started
===============

The Ebook_homebrew is a python package, so that you can use ``setup.py`` or ``pip`` installer.

Using setup.py
--------------

.. code-block:: bash

   $ python setup.py install

Or using pip installer
----------------------

.. code-block:: bash

   $ pip install ebook-homebrew

Usage
=====

You can use global command ``ebookhomebrew`` .

Show help.

.. code-block:: bash

   $ ebookhomebrew -h

Ex) Rename image file to only digit and Create PDF file.

.. code-block:: bash

   $ ebookhomebrew auto -s ./tests -d 3,4 -e jpg -f test.pdf

ebookhomebrew command line interface
------------------------------------

You can use ebookhomebrew command line interface.

Subcommands
^^^^^^^^^^^

.. code-block:: bash

     Choose subcommands. Usually choose "auto"
     {auto}
      auto      Make only digit file name, convert e-book file such as PDF

Options
^^^^^^^

.. code-block:: bash

   -h, --help            show this help message and exit
   -s SRC_DIR, --src_dir SRC_DIR
                         Source directory which put original image files.
   --dst_dir DST_DIR     Destination directory which put e-book file.
   -d N,N, --digit N,N   Serial number digits you remain file name
   -e EXT, --extension EXT
                         Destination directory which put e-book file.
   -f FILENAME, --filename FILENAME
                         Destination directory which put e-book file.
   -m, --manual          Duplicate file name, solving manually.
   -r, --remove          Remove original image file.
   -y, --assume_yes      no verify users.

Testing
=======

Unit Test
---------

Using pytest, if you want to test.

.. code-block:: bash

   $ pytest

If you get coverage report, run coverage and report.

.. code-block:: bash

   $ coverage run --source=ebook_homebrew -m pytest
   $ coverage report -m

Or pytest-cov param for pytest

.. code-block:: bash

   $ pytest --cov=ebook_homebrew --cov-report html --cov-report xml

Integration Test
----------------

Using pytest, if you want to test with mark "--it"

.. code-block:: bash

   $ pytest --it

With tox
--------

With tox, you can test multiple python version.(only python3.5, 3.6)

.. code-block:: bash

   $ tox

Travis-CI
---------

This repository uses `Travis-CI <https://travis-ci.org/>`_ and be building jobs by push or PR branches.

Licence
=======

This software is released under the MIT License, see LICENSE.

API Document
============

The `Document <https://ebook-homebrew.readthedocs.io/en/latest/>`_ write by Sphinx.
