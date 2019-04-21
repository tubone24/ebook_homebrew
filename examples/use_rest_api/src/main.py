"""
Overview:
  Client App with ebook-homebrew's rest API

Usage:
  main.py [-h|--help] [-v|--version]
  main.py upload [--host <host>] [--port <port>] <directory>
  main.py convert [--host <host>] [--port <port>] <id>
  main.py download [--host <host>] [--port <port>] <id>

Options:
  -h, --help     : show this help message and exit
  -v, --version  : show version
  --host         : API server host
  --port         : API server port
"""

import requests
from docopt import docopt

__version__ = "2.0.0"


def main(args):
    if args["upload"]:
        pass
    elif args["convert"]:
        pass
    elif args["download"]:
        pass
    elif args["--version"]:
        show_version()


def _open_image_file():
    pass


def show_version():
    print("ebook-homebrew Rest Client: {version}".format(version=__version__))


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
