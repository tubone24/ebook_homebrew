# -*- coding: utf-8 -*-
"""Convert file format.
"""
import os
import re

import PIL.Image
import PyPDF2

from .core import Common
from .exceptions import InvalidImageFileFormatError
from .utils.logging import get_logger

logger = get_logger("image2pdf")


class Image2PDF(Common):
    """Make pdf file for using e-books.

    """

    def __init__(self, digits, extension, directory_path=None):
        """Constructor

        Args:
            digits (str): Regex target digit.
            extension (str): Target file extension.
            directory_path (str): Target directory path.
        """
        super().__init__()
        self.__digits = digits
        self.__extension = self._convert_extension_with_dot(extension)
        self.__regex_ext = re.compile(self.__extension)
        self.__file_writer = PyPDF2.PdfFileWriter()
        if directory_path is not None:
            self.__directory_path = directory_path
        else:
            self.__directory_path = os.getcwd()
            logger.debug("Current Directory: {cwd}".format(cwd=self.__directory_path))
        os.chdir(self.__directory_path)

    def make_pdf(self, filename, remove_flag=False):
        """Make pdf file take in some image files.

        Make pdf file which you use e-books by take in some image
        files such as jpeg, png and gif.

        Args:
            filename (str): pdf file name
            remove_flag (bool): If true, original image file is deleted

        Returns:
            bool: If success, return true.

        """
        self._check_image_extension(self.__extension)

        files = self._make_file_list(self.__directory_path, sort=True)
        logger.debug("files: {files}".format(files=files))
        page_count = 0
        remove_files = []

        for file in files:
            num = self._check_serial_number(file, self.__digits)
            if self._check_skip_file(file, self.__regex_ext, num):
                pass
            else:
                pdf_file = self._convert_image_to_pdf(file)

                if self._merge_pdf_file(pdf_file, filename):
                    logger.info(
                        "Success write pdf for {page} page.".format(page=page_count + 1)
                    )
                    page_count += 1
                    if remove_flag:
                        remove_files.append(file)
        logger.info("-" * 55)
        if page_count == 0:
            logger.warn("Target file doesn't exist... Finish.")
            return False
        logger.info(
            "All image file are converted. Filename: {filename}".format(
                filename=filename
            )
        )
        if self._remove_file_bulk(remove_files):
            logger.info("Post possess is finished")
        return True

    def _convert_image_to_pdf(self, file, resolution=100.0):
        """Convert Image file to pdf file format.

        Args:
            file (str): Image file
            resolution (float): Pdf file resolution, default 100.

        Returns:
            str: Convert pdf file name.
        """
        image = PIL.Image.open(file).convert("RGB")
        pdf_file_name = file.replace(self.__extension, ".pdf")
        image.save(pdf_file_name, "PDF", resolution=resolution)
        return pdf_file_name

    @staticmethod
    def _check_image_extension(extension):
        """ Check image file extension or not.

        Args:
            extension (str): Image file extension
        Returns:
            bool: If extension is image file, return true.
        Raises:
            InvalidImageFileFormatError: If extension is not image file.
        """
        if extension not in (".jpg", ".png", ".gif"):
            raise InvalidImageFileFormatError()
        return True

    def _merge_pdf_file(self, pdf_file, filename):
        """Marge pdf files.

        Args:
            pdf_file (str): 1 page pdf file
            filename (str): Merge target pdf file name

        Returns:
            bool: If success, return true.

        """
        logger.debug(type(pdf_file))
        with open(pdf_file, "rb") as f:
            file_reader = PyPDF2.PdfFileReader(f)
            self.__file_writer.addPage(file_reader.getPage(0))
            logger.debug("Merge {pdf_file}".format(pdf_file=pdf_file))
            self._write_pdf(filename)
        self._remove_file(pdf_file, assume_yes=True)
        return True

    def _write_pdf(self, file_name):
        """Write pdf file

        Args:
            file_name (str): pdf file name.

        Returns:
            If success, return true.

        """
        with open(file_name, "wb") as f:
            self.__file_writer.write(f)
        return True
