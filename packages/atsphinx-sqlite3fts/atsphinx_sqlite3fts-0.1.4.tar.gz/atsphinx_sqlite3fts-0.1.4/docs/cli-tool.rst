===============
Simple CLI tool
===============

``atsphinx-sqlite3fts`` provides simple CLI tool to display result of searching.

Requirements
============

If you want to use CLI tool, it need ``Click`` library.
You can insallt ``atsphinx-sqlite3fts`` with extra packages.

.. code-block:: console

   pip install 'atsphinx-sqlite3fts[cli]'

Usage example
=============

Before run CLI, build database by ``sphinx-build``.

.. code-block:: console

   sphinx-build -b sqlite . _build

To search from database, run command with path of database and keyword.

.. code-block:: console

   atsphinx-sqlite3fts _build/db.sqlite Hello

   cli-tool
        Simple CLI tool

   getting-started
        Getting started

Command display pagename and title.
