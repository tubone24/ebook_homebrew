from unittest.mock import patch

from ebook_homebrew.helper import show_version
from ebook_homebrew.__init__ import __version__


def test_show_version():
    with patch("builtins.print") as mock_print:
        show_version()
        mock_print.assert_called_once_with("ebook_homebrew: {version}".format(version=__version__))
