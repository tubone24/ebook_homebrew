import pytest
from unittest.mock import call
from unittest.mock import patch
import logging

from ebook_homebrew.core import Common
from ebook_homebrew.exceptions import InvalidExtensionType, \
    InvalidPathType, InvalidDigitsFormat, ChangeFileNameOSError, InvalidImageParameterType


_logger = logging.getLogger(name=__name__)


class TestCommon(object):
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))
        self.target = Common()

    @pytest.mark.parametrize("test_input, expected", [
        ("jpg", ".jpg"),
        (".png", ".png"),
        (".part1.rar", ".part1.rar"),
        ("part1.rar", ".part1.rar"),
        (10, ".10"),
        (0.42, ".0.42")])
    def test_ok__convert_extension_with_dot(self, test_input, expected):
        actual = self.target._convert_extension_with_dot(test_input)
        _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
        assert actual == expected

    @pytest.mark.parametrize("test_input", [["jpg"],
                                            {},
                                            None])
    def test_error__convert_extension_with_dot(self, test_input):
        with pytest.raises(InvalidExtensionType):
             self.target._convert_extension_with_dot(test_input)

    @pytest.mark.parametrize("test_input, expected", [
        ("/usr/local/common/test.py", ("/usr/local/common", "test", ".py")),
        ("../tests/python3.6.txt", ("../tests", "python3.6", ".txt")),
        ("example.nim", ("", "example", ".nim"))])
    def test_ok__split_dir_root_ext(self, test_input, expected):
        actual = self.target._split_dir_root_ext(test_input)
        _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
        assert actual == expected

    def test_error__split_dir_root_ext(self):
        test_input = 32.445
        with pytest.raises(InvalidPathType):
            self.target._split_dir_root_ext(test_input)

    @pytest.mark.parametrize("test_input, expected", [
        (("test001.txt", 3), "001"),
        (("hoge00234foo.py", "3,5"), "00234"),
        (("barbar002345foo.py", "3,4"), "0023")])
    def test_ok__check_serial_number(self, test_input, expected):
        actual = self.target._check_serial_number(*test_input).group(0)
        _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
        assert actual == expected

    def test_unmatched__check_serial_number(self):
        test_input = ("hogefoobar.js", 3)
        actual = self.target._check_serial_number(*test_input)
        assert actual is None

    @pytest.mark.parametrize("test_input, expected", [
        ("3,4", 4),
        ("3", 3),
        ("3,5", 5)])
    def test_ok__check_digit_format(self, test_input, expected):
        actual = self.target._check_digit_format(test_input)
        _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
        assert actual == expected

    @pytest.mark.parametrize("test_input", [
        4,
        "3, 4",
        3.5])
    def test_error__check_digit_format(self, test_input):
        with pytest.raises(InvalidDigitsFormat):
            self.target._check_digit_format(test_input)

    def test_ok__rename_file(self):
        with patch("os.rename") as mock_rename:
            actual = self.target._rename_file("foo", "bar")
            mock_rename.assert_called_once_with("foo", "bar")
            expected = True
            _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
            assert actual is expected

    def test_error__rename_file(self):
        with patch("os.rename") as mock:
            mock.side_effect = OSError
            with pytest.raises(ChangeFileNameOSError):
                self.target._rename_file("foo", "bar")

    @pytest.mark.parametrize("input_param, expected", [
        ("Y", True),
        ("y", True),
        ("n", False),
        ("N", False),
        ("hoge", False)])
    def test_ok__remove_file(self, input_param, expected):
        with patch("os.remove") as mock_remove:
            with patch("builtins.input") as mock_input:
                mock_input.return_value = input_param
                actual = self.target._remove_file("foo", assume_yes=False)
                if expected is True:
                    mock_remove.assert_called_once_with("foo")
                _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
                assert actual is expected

    def test_ok__remove_file_with_assume_yes(self):
        with patch("os.remove") as mock_remove:
            actual = self.target._remove_file("foo", assume_yes=True)
            mock_remove.assert_called_once_with("foo")
            expected = True
            _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
            assert actual is expected

    @pytest.mark.parametrize("test_input, called, input_param, expected", [
        (("foo", "/bar1/bar2"), ("foo", "/bar1"), "Y", True),
        (("foo", "/bar1/bar2"), ("foo", "/bar1"), "y", True),
        (("foo", "bar3"), ("foo", ""), "Y", True),
        (("foo", "bar3"), ("foo", ""), "y", True),
        (("foo", "bar1/bar2"), ("foo", "/bar1"), "n", False),
        (("foo", "bar1/bar2"), ("foo", "/bar1"), "N", False),
        (("foo", "bar1/bar2"), ("foo", "/bar1"), "hoge", False)])
    def test_ok__move_file(self, test_input, called, input_param, expected):
        with patch("shutil.move") as mock_move:
            with patch("builtins.input") as mock_input:
                mock_input.return_value = input_param
                actual = self.target._move_file(*test_input, assume_yes=False)
                if expected is True:
                    mock_move.assert_called_once_with(*called)
                _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
                assert actual is expected

    def test_ok__move_file_with_assume_yes(self):
        with patch("shutil.move") as mock_move:
            actual = self.target._move_file("foo", "/bar1/bar2", assume_yes=True)
            mock_move.assert_called_once_with("foo", "/bar1")
            expected = True
            _logger.debug("\nactual:   {actual}\nexpected: {expected}".format(actual=actual, expected=expected))
            assert actual is expected

    @pytest.mark.parametrize("test_input, calls, expected", [
        (["foo", "bar"], [call("foo"), call("bar")], True),
        (["foo", "bar", "hoge"], [call("foo"), call("bar"), call("hoge")], True),
        (["foo"], [call("foo")], True),
        ([], [], False),
        (None, [], False)])
    def test_ok__remove_file_bulk(self, test_input, calls, expected):
        with patch("os.remove") as mock_remove:
            actual = self.target._remove_file_bulk(test_input)
            if expected is True:
                assert mock_remove.call_args_list == calls
            assert actual is expected

    @pytest.mark.parametrize("test_input, expected", [
        ("test.jpg", None),
        ("test.png", None),
        ("test.gif", None)])
    def test_ok__check_image_file(self, test_input, expected):
        with patch("PIL.Image.open") as mock_pil_open:
            with patch("PIL.Image.open.show"):
                actual = self.target._check_image_file(test_input)
                mock_pil_open.assert_called_once_with(test_input)
                assert actual == expected

    def test_error__check_image_file(self):
        test_input = "test.txt"
        with patch("PIL.Image.open"):
            with patch("PIL.Image.open.show"):
                with pytest.raises(InvalidImageParameterType):
                    self.target._check_image_file(test_input)






