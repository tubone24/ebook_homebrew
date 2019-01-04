import re
import pytest
import logging
from ebook_homebrew.core import Common
from ebook_homebrew.exceptions import InvalidExtensionType, InvalidPathType

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










