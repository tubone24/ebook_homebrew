import logging
import zipfile
from unittest.mock import patch

import pytest

from ebook_homebrew.archive import MakeArchive
from ebook_homebrew.exceptions import ZipFileExistError

_logger = logging.getLogger(name=__name__)


class TestMakeArchive(object):

    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))
        with patch("os.chdir") as mock_chdir:
            self.target = MakeArchive(directory_path="test", extension="jpg")
            mock_chdir.assert_called_once_with("test")

    def test_init_current_dir(self):
        with patch("os.chdir") as mock_chdir, \
                patch("os.getcwd", return_value="tests") as mock_getcwd:
            MakeArchive(extension="jpg")
            mock_getcwd.assert_called_once_with()
            mock_chdir.assert_called_once_with("tests")

    @pytest.mark.parametrize("test_input_filename, test_input_remove_flag, test_input_overwrite_flag, filelist", [
        ("test.zip", False, False, ["test001.jpg"]),
        ("test.zip", True, False, ["test001.jpg"]),
        ("test.zip", False, True, ["test001.jpg"]),
        ("test.zip", True, True, ["test001.jpg"])])
    def test_make_zip(self, test_input_filename, test_input_remove_flag, test_input_overwrite_flag, filelist):
        expected = True
        with patch("os.listdir", return_value=filelist) as mock_list_dir, \
                patch("zipfile.ZipFile") as mock_zipfile, \
                patch.object(self.target, "_remove_file") as mock_remove_file:
            actual = self.target.make_zip(test_input_filename, test_input_remove_flag, test_input_overwrite_flag)
            mock_list_dir.assert_called_once_with("test")
            if test_input_overwrite_flag:
                file_mode = "w"
            else:
                file_mode = "x"
            mock_zipfile.assert_called_once_with(test_input_filename, file_mode, zipfile.ZIP_DEFLATED)
            mock_zipfile().__enter__().write.assert_called_once_with(*filelist)
            if test_input_remove_flag:
                mock_remove_file.assert_called_once_with(*filelist, assume_yes=True)
            assert actual == expected

    def test_skip_extension_make_zip(self):
        file_list = ["test001.txt"]
        expected = True
        with patch("os.listdir", return_value=file_list):
            actual = self.target.make_zip("test.zip", False, False)
            assert actual == expected

    def test_error_make_zip(self):
        file_list = ["test001.jpg"]
        with patch("os.listdir", return_value=file_list), patch("zipfile.ZipFile", side_effect=FileExistsError):
            with pytest.raises(ZipFileExistError):
                self.target.make_zip("test.zip", False, False)
