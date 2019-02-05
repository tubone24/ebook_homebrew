import logging
import os
from time import time
import shutil
from unittest.mock import patch

import pytest

from ebook_homebrew.rename import ChangeFilename

_logger = logging.getLogger(name=__name__)


class TestItRename(object):

    @staticmethod
    def copy_image_file(directory):
        test_file = os.path.join(os.path.dirname(__file__), "assets", "test_image.png")
        for i in range(100):
            shutil.copy2(test_file, directory)
            dst_file_name = os.path.join(directory, "foo" + str(i).zfill(3) + "bar.png")
            os.rename(os.path.join(directory, "test_image.png"), dst_file_name)
        shutil.copy2(test_file, directory)
        dst_ext_file_name = os.path.join(directory, "foofoo001" + "b_bar.png")
        os.rename(os.path.join(directory, "test_image.png"), dst_ext_file_name)
        return True

    @staticmethod
    def interactive_input():
        for out in ["y", "test.png"]:
            yield out

    @pytest.mark.it
    def test_it_rename(self, tmpdir):
        _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=tmpdir))
        self.copy_image_file(str(tmpdir))
        rename_ins = ChangeFilename(directory_path=str(tmpdir), digits="3", extension="png")
        start_time = time()
        actual = rename_ins.filename_to_digit_number()
        end_time = time()
        assert len(actual) == 1

        with patch("builtins.input") as mock_input:
            mock_input.side_effect = self.interactive_input()
            actual = rename_ins.change_name_manually(overwrite=True)
            assert actual is True

        actual = rename_ins.add_before_after_str("foo", "bar")
        assert actual is True

        actual_file_list = set(os.listdir(str(tmpdir)))
        expected = {"foo" + str(x).zfill(3) + "bar.png" for x in range(100)}
        actual = actual_file_list - expected
        assert actual == {"test.png"}
        _logger.info("filename_to_digit_number spent: {} s".format(end_time - start_time))

    @pytest.mark.it
    def test_it_async_rename(self, tmpdir):
        _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=tmpdir))
        self.copy_image_file(str(tmpdir))
        rename_ins = ChangeFilename(directory_path=str(tmpdir), digits="3", extension="png")
        start_time = time()
        actual = rename_ins.async_filename_to_digit_number()
        end_time = time()
        assert len(actual) == 1
        _logger.info("async_filename_to_digit_number spent: {} s".format(end_time - start_time))