from unittest.mock import patch

import pytest

from ebook_homebrew import helper as target
from ebook_homebrew.__init__ import __version__

class ArgNameSpace(object):
    def __init__(self):
        self.src_dir = []
        self.dst_dir = []
        self.digit = []
        self.extension = []
        self.filename = []
        self.manual = False
        self.assume_yes = False
        self.remove = False
        self.port = []

def test_show_version():
    with patch("builtins.print") as mock_print:
        target.show_version()
        mock_print.assert_called_once_with("ebook_homebrew: {version}".format(version=__version__))


def test_rest_api():
    args = ArgNameSpace()
    args.port.append(8080)
    with patch.object(target, "api") as mock_api:
        target.rest_api(args)
        mock_api.run.assert_called_once_with(address="0.0.0.0", port=8080)
