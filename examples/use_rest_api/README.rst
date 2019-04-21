=========================================
Client App with ebook-homebrew's rest API
=========================================

Client App with ebook-homebrew's rest API interface.

Getting Started
===============

Needs ``requests`` and ``docopt`` .

.. code-block:: bash

   $ pip install requirements.txt

Usage
=====

Run ``CLI`` .

.. code-block:: bash

   $ cd src
   $ python main.py -h

   Usage:
    main.py [-h|--help] [-v|--version]
    main.py upload <directory> <extension> [--host <host>] [--port <port>]
    main.py convert <id> <extension> [--host <host>] [--port <port>]
    main.py download <id> <file> [--host <host>] [--port <port>]

   Options:
    upload         : upload
    convert        : convert
    <directory>    : directory
    <extension>    : extension
    <id>           : upload_id
    <file>         : filename
    -h, --help     : show this help message and exit
    -v, --version  : show version
    --host         : API server host
    --port         : API server port

