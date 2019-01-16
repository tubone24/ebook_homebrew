import logging
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

import pytest

from ebook_homebrew import cli
from ebook_homebrew.cli import main
from ebook_homebrew.cli import execute_auto

_logger = logging.getLogger(name=__name__)


class TestCli(object):

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

    @pytest.fixture
    def args_ok(self):
        args_obj = self.ArgNameSpace()
        args_obj.src_dir.append("test_src")
        args_obj.dst_dir.append("test_dst")
        args_obj.digit.append("3")
        args_obj.extension.append("png")
        args_obj.filename.append("test.pdf")
        args_obj.manual = True
        args_obj.assume_yes = True
        args_obj.remove = True
        return args_obj

    def test_execute_auto(self, args_ok):
        with patch.object(cli, "auto") as mock_auto:
            execute_auto(args_ok)
            mock_auto.assert_called_once_with(args_ok)

    def test_main_set_args(self):
        mock_parser = MagicMock(name="mock_parser")
        mock_subparser = MagicMock(name="mock_subparser")
        mock_parser_auto = MagicMock(name="mock_parser_auto")
        mock_args = MagicMock(name="mock_args")
        with patch("argparse.ArgumentParser", return_value=mock_parser) as mock_ArgumentParser:
            mock_parser.add_subparsers.return_value = mock_subparser
            mock_parser.parse_args.return_value = mock_args
            mock_subparser.add_parser.return_value = mock_parser_auto
            main()
            mock_ArgumentParser.assert_called_once_with(prog="ebook_homebrew",
                                                        usage="ebookhomebrew",
                                                        description="You can make e-books for some image files",
                                                        epilog="More information? Access here: "
                                                               "https://github.com/tubone24/ebook_homebrew",
                                                        add_help=True)
            mock_parser.add_subparsers.assert_called_once_with(description="Choose subcommands. "
                                                                           "Usually choose \"auto\"")
            mock_parser.add_argument.assert_called_once_with("-v", "--version",
                                                             action="store_true",
                                                             help="Show version")
            calls_subparser = [
                call("auto",
                     description="Make only digit file name, "
                                 "convert e-book file such as PDF",
                     help="Make only digit file name, "
                          "convert e-book file such as PDF"),
                call("makezip",
                     description="Make zip file for files "
                                 "which you choose extension.",
                     help="Make zip file for adding specify extension files.")]
            mock_subparser.add_parser.assert_has_calls(calls_subparser)
            mock_parser_auto.set_defaults.assert_called_once_with(handler=execute_auto)
            calls_parser_auto = [call("-s", "--src_dir",
                                      action="store",
                                      nargs=1,
                                      const=None,
                                      default=None,
                                      required=True,
                                      type=str,
                                      help="Source directory which put original image files.",
                                      metavar="SRC_DIR"),
                                 call("--dst_dir",
                                      action="store",
                                      nargs=1,
                                      const=None,
                                      default=None,
                                      type=str,
                                      help="Destination directory which put e-book file.",
                                      metavar="DST_DIR"),
                                 call("-d", "--digit",
                                      action="store",
                                      nargs=1,
                                      const=None,
                                      default=None,
                                      required=True,
                                      type=str,
                                      help="Serial number digits you remain file name",
                                      metavar="N,N"),
                                 call("-e", "--extension",
                                      action="store",
                                      nargs=1,
                                      const=None,
                                      default=None,
                                      required=True,
                                      type=str,
                                      help="Destination directory which put e-book file.",
                                      metavar="EXT"),
                                 call("-f", "--filename",
                                      action="store",
                                      nargs=1,
                                      const=None,
                                      default=None,
                                      required=True,
                                      type=str,
                                      help="Destination directory which put e-book file.",
                                      metavar="FILENAME"),
                                 call("-m", "--manual",
                                      action="store_true",
                                      help="Duplicate file name, solving manually."),
                                 call("-r", "--remove",
                                      action="store_true",
                                      help="Remove original image file."),
                                 call("-y", "--assume_yes",
                                      action="store_true",
                                      help="no verify users.")]
            mock_parser_auto.add_argument.assert_has_calls(calls_parser_auto)
            mock_parser.parse_args.assert_called_once_with()
            mock_args.handler.assert_called_once_with(mock_args)
