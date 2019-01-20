import logging
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from ebook_homebrew.convert import Image2PDF
from ebook_homebrew.exceptions import InvalidImageFileFormatError

_logger = logging.getLogger(name=__name__)


class TestImage2PDF(object):
    def setup_method(self, method):
        _logger.info("method{}".format(method.__name__))
        with patch("PyPDF2.PdfFileWriter"), patch("os.chdir") as mock_chdir:
            self.target = Image2PDF(directory_path="test", digits="3", extension="jpg")
            mock_chdir.assert_called_once_with("test")

    def test_init_current_dir(self):
        with patch("PyPDF2.PdfFileWriter"), patch("os.chdir") as mock_chdir, \
                patch("os.getcwd", return_value="tests") as mock_getcwd:
            Image2PDF(digits="3", extension="jpg")
            mock_getcwd.assert_called_once_with()
            mock_chdir.assert_called_once_with("tests")

    def test__convert_image_to_pdf(self):
        expected = "test.pdf"
        with patch("PIL.Image.open") as mock_image_open:
            mock_image = MagicMock()
            mock_image_open.return_value = mock_image
            mock_image_converted = MagicMock()
            mock_image.convert.return_value = mock_image_converted
            actual = self.target._convert_image_to_pdf("test.jpg", resolution=100.0)
            mock_image_open.assert_called_once_with("test.jpg")
            mock_image.convert.assert_called_with("RGB")
            mock_image_converted.save.assert_called_with(expected, "PDF", resolution=100.0)
            assert actual == expected

    def test__write_pdf(self):
        test_input = "test.pdf"
        expected = True
        with patch("builtins.open") as mock_open, \
                patch.object(self.target, "_Image2PDF__file_writer") as mock_pdf_writer:
            actual = self.target._write_pdf(test_input)
            mock_open.assert_called_once_with(test_input, "wb")
            mock_pdf_writer.write.assert_called_once_with(mock_open().__enter__())
            assert actual == expected

    def test__merge_pdf_file(self):
        test_input_pdf_file = "test001.pdf"
        test_input_filename = "foobar.pdf"
        expected = True
        with patch("builtins.open") as mock_open, \
                patch("PyPDF2.PdfFileReader") as mock_pdf_reader, \
                patch.object(self.target, "_Image2PDF__file_writer") as mock_pdf_writer, \
                patch.object(self.target, "_write_pdf") as mock_write_pdf, \
                patch.object(self.target, "_remove_file") as mock_remove_file:
            mock_file_reader = MagicMock(name="file_reader")
            mock_pdf_reader.return_value = mock_file_reader

            actual = self.target._merge_pdf_file(test_input_pdf_file, test_input_filename)

            mock_open.assert_called_once_with(test_input_pdf_file, "rb")
            mock_file_reader.getPage.assert_called_once_with(0)
            mock_pdf_writer.addPage.assert_called_once_with(mock_file_reader.getPage())
            mock_write_pdf.assert_called_once_with(test_input_filename)
            mock_remove_file.assert_called_once_with(test_input_pdf_file, assume_yes=True)
            assert actual == expected

    @pytest.mark.parametrize("test_input_filename, test_input_remove_flag, filelist, pdf_file_name, expected", [
        ("test.pdf", False, ["test001.jpg"], "test001.pdf", True),
        ("test.pdf", True, ["test001.jpg"], "test001.pdf", True)])
    def test_ok_make_pdf(self, test_input_filename, test_input_remove_flag, filelist, pdf_file_name, expected):
        with patch("os.listdir") as mock_list_dir, \
                patch.object(self.target, "_convert_image_to_pdf") as mock_convert_image_to_pdf, \
                patch.object(self.target, "_merge_pdf_file") as mock_merge_pdf_file, \
                patch.object(self.target, "_remove_file_bulk") as mock_remove_file_bulk:
            mock_list_dir.return_value = filelist
            mock_convert_image_to_pdf.return_value = pdf_file_name
            mock_merge_pdf_file.return_value = True
            mock_remove_file_bulk.return_value = True
            actual = self.target.make_pdf(test_input_filename, test_input_remove_flag)
            mock_convert_image_to_pdf.assert_called_with(*filelist)
            mock_merge_pdf_file.assert_called_with(pdf_file_name, test_input_filename)
            if test_input_remove_flag:
                mock_remove_file_bulk.assert_called_with(filelist)
            assert actual == expected

    @pytest.mark.parametrize("test_input_filename, test_input_remove_flug, filelist, expected", [
        ("test.pdf", False, ["test001.png"], False),
        ("test.pdf", True, ["test001.png"], False),
        ("test.pdf", False, ["testfoo.jpg"], False)])
    def test_skip_make_pdf(self, test_input_filename, test_input_remove_flug, filelist, expected):
        with patch("os.listdir") as mock_list_dir, \
                patch.object(self.target, "_remove_file_bulk") as mock_remove_file_bulk:
            mock_list_dir.return_value = filelist
            mock_remove_file_bulk.return_value = True
            actual = self.target.make_pdf(test_input_filename, test_input_remove_flug)
            if test_input_remove_flug:
                mock_remove_file_bulk.assert_not_called()
            assert actual == expected

    def test_error_make_pdf(self):
        with patch("PyPDF2.PdfFileWriter"), patch("os.chdir") as mock_chdir:
            target = Image2PDF(directory_path="test", digits="3", extension="txt")
            mock_chdir.assert_called_once_with("test")
        with pytest.raises(InvalidImageFileFormatError):
            target.make_pdf("test.pdf", False)

    @pytest.mark.parametrize("test_input_extension", [
        ".jpg",
        ".png",
        ".gif"])
    def test_ok_check_image_extension(self, test_input_extension):
        expected = True
        actual = self.target._check_image_extension(test_input_extension)
        assert actual == expected

    def test_error_check_image_extension(self):
        with pytest.raises(InvalidImageFileFormatError):
            self.target._check_image_extension(".txt")
