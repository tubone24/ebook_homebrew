import pytest
from unittest.mock import call
from unittest.mock import patch
import logging

from ebook_homebrew.convert import Image2PDF

_logger = logging.getLogger(name=__name__)


class TestImage2PDF(object):
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))
        with patch("PyPDF2.PdfFileWriter"):
            self.target = Image2PDF(directory_path="test", digits="3", extension="jpg")