import logging
import re
from unittest.mock import patch

import pytest

from ebook_homebrew.exceptions import InvalidNumberParameterType, \
    TargetSrcFileNotFoundError, ChangeFileNameOSError, InvalidImageParameterType
from ebook_homebrew.rename import ChangeFilename

_logger = logging.getLogger(name=__name__)


class TestChangeFilename(object):

    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))
        with patch("os.chdir"):
            self.target = ChangeFilename(directory_path="test", digits="3", extension="jpg")

    @pytest.mark.parametrize("test_input, expected", [
        (["test001.jpg", 5], "00001.jpg"),
        (["test001foo2.jpg", 5], "00001.jpg"),
        (["001.jpg", 3], "001.jpg"),
        (["001.jpg", 2], "001.jpg")])
    def test_ok_create_new_name(self, test_input, expected):
        match_obj = re.search("\\d{3}", test_input[0])
        actual = self.target._create_new_name(match_obj, test_input[1], ".jpg")
        assert actual == expected

    def test_error_create_new_name(self):
        with pytest.raises(InvalidNumberParameterType):
            self.target._create_new_name("test", 5, ".jpg")

    @pytest.mark.parametrize("file_list, is_file, expected", [
        (["test001test.jpg", "test002foo.jpg"], False, 0),
        (["test001test.jpg", "test002foo.png"], False, 0),
        (["test001test.jpg", "testfoobar.jpg"], False, 0),
        (["test001test.jpg", "test001foo.jpg"], True, 2),
        ([], False, 0)])
    def test_ok_filename_to_digit_number(self, file_list, is_file, expected):
        with patch("os.listdir") as mock_listdir, patch("os.path.isfile") as mock_isfile, \
                patch.object(self.target, "_rename_file"):
            mock_listdir.return_value = file_list
            mock_isfile.return_value = is_file
            actual = self.target.filename_to_digit_number()
            assert len(actual) is expected
            mock_listdir.assert_called_once_with("test")

    def test_file_not_found_error_filename_to_digit(self):
        with patch("os.listdir") as mock_listdir:
            mock_listdir.side_effect = FileNotFoundError
            with pytest.raises(TargetSrcFileNotFoundError):
                self.target.filename_to_digit_number()

    def test_os_error_filename_to_digit(self):
        with patch("os.listdir") as mock_listdir, patch("os.path.isfile") as mock_isfile:
            mock_listdir.return_value = ["test001foo.jpg"]
            mock_isfile.side_effect = OSError
            with pytest.raises(ChangeFileNameOSError):
                self.target.filename_to_digit_number()

    @staticmethod
    def interactive_input(test_input):
        for out in test_input:
            yield out

    @pytest.mark.parametrize("test_interactive, is_file_return, expected", [
        (["y", "foo.jpg"], [True, False], True),
        (["Y", ""], [True, False], True),
        (["Y", "foo.jpg", "bar.jpg"], [True, True, False], True),
        (["N", ""], [True, False], True),
        (["r", "y", "y"], [True, False], True),
        (["r", "r", "foo.jpg"], [True, False, False], True),
        (["r", "c"], [True, False], True),
        (["r", "n"], [True, False], True)])
    def test_ok_change_name_manually(self, test_interactive, is_file_return, expected):
        with patch("os.listdir") as mock_listdir, patch("os.path.isfile") as mock_isfile, \
                patch.object(self.target, "_rename_file"), \
                patch("builtins.input") as mock_input, \
                patch.object(self.target, "_remove_file"), \
                patch.object(self.target, "_check_image_file"):
            mock_listdir.return_value = ["test001test.jpg"]
            mock_isfile.side_effect = is_file_return
            mock_input.side_effect = self.interactive_input(test_interactive)
            self.target.filename_to_digit_number()
            actual = self.target.change_name_manually(overwrite=False)
            assert actual == expected

    @pytest.mark.parametrize("test_interactive, is_file_return", [
        (["r", "c"], [True, False])])
    def test_skip_change_name_manually(self, test_interactive, is_file_return):
        with patch("os.listdir") as mock_listdir, patch("os.path.isfile") as mock_isfile, \
                patch("builtins.input") as mock_input, \
                patch.object(self.target, "_check_image_file") as mock_image:
            mock_listdir.return_value = ["test001test.jpg"]
            mock_isfile.side_effect = is_file_return
            mock_input.side_effect = self.interactive_input(test_interactive)
            mock_image.side_effect = InvalidImageParameterType
            self.target.filename_to_digit_number()
            actual = self.target.change_name_manually(overwrite=False)
            assert actual is True

    @pytest.mark.parametrize("test_file_list, is_file_return, test_input", [
        (["001.jpg", "002.jpg"], False, ["foo", "bar"]),
        (["001.jpg", "002.jpg"], False, ["foo", None]),
        (["001.jpg", "002.jpg"], False, [None, "bar"]),
        (["001.jpg", "002.txt"], False, ["foo", "bar"]),
        (["001.jpg", "aaa.jpg"], True, ["foo", "bar"]),
        (["001.jpg", "foo001bar.jpg"], [False, True], ["foo", "bar"])])
    def test_add_before_after_str(self, test_file_list, is_file_return, test_input):
        with patch("os.listdir") as mock_listdir, patch("os.path.isfile") as mock_isfile, \
                patch.object(self.target, "_rename_file"):
            mock_listdir.return_value = test_file_list
            mock_isfile.return_value = is_file_return
            actual = self.target.add_before_after_str(*test_input)
            assert actual is True
