import pytest
from unittest.mock import call
from unittest.mock import patch
import logging

from ebook_homebrew.convert import Image2PDF

_logger = logging.getLogger(name=__name__)


class TestImage2PDF(object):
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))
        with patch("PyPDF2.PdfFileWriter"), patch("os.chdir"):
            self.target = Image2PDF(directory_path="test", digits="3", extension="jpg")

    def test__convert_image_to_pdf(self):
        with patch("PIL.Image.open") as mock_image_open:
            mock_image_open.convert.return_value = True
            mock_image_open.save.return_value = True
            actual = self.target._convert_image_to_pdf("test.jpg")
            assert actual == "test.pdf"

    def test_ok_make_pdf(self):
        with patch("os.listdir") as mock_list_dir:
            mock_list_dir.return_value = ["test001.jpg", "test002.jpg", "test003.txt"]