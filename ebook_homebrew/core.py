# -*- coding: utf-8 -*-
"""Core module
"""
import os
import re
import shutil

import PIL.Image

from .exceptions import InvalidDigitsFormat, ChangeFileNameOSError, \
    InvalidImageParameterType, InvalidExtensionType, InvalidPathType
from .utils.logging import get_logger

logger = get_logger("Core")


class Common(object):
    """Common Class
    """

    def __init__(self):
        pass

    @staticmethod
    def _convert_extension_with_dot(extension):
        """Convert extension with dot like "jpg" to ".jpg"

        Args:
            extension (str): Convert extension with dot like "jpg" to ".jpg"

        Returns:
            str: Convert extension with dot like "jpg" to ".jpg"
        """
        try:
            if type(extension) is str:
                pass
            elif type(extension) is int:
                extension = str(extension)
            elif type(extension) is float:
                extension = str(extension)
            else:
                raise TypeError

            if re.match(r"^\..+", extension):
                return extension
            else:
                extension_with_dot = "." + extension
                return extension_with_dot
        except TypeError:
            raise InvalidExtensionType()

    @staticmethod
    def _split_dir_root_ext(path):
        """Split file path to "directory", "file_root" and "extension"

        Args:
            path (str): File path like "/usr/local/common/test.py"

        Returns:
            str: Directory like "/usr/local/common"
            str: file_root like "test"
            str: extension like ".py"
        """
        try:
            dir_name = os.path.dirname(path)
            base_name = os.path.basename(path)
            base_root, ext = os.path.splitext(base_name)
            return dir_name, base_root, ext
        except (TypeError, AttributeError):
            raise InvalidPathType()

    @staticmethod
    def _check_serial_number(filename, digits):
        """Check filename contains "digit" like "foo001.txt" and return match object"

        Args:
            filename (str): filename you can check "digit"
            digits (str): Regex format like "3,5"

        Returns:
            Match: If filename contains digit, return Match object, others return false.
        """
        match_obj = re.search("\\d{" + str(digits) + "}", filename)
        return match_obj

    @staticmethod
    def _check_digit_format(digits):
        """Check digit matched Regex format and return max digit number.

        Args:
            digits (str): Digit you will check regex

        Returns:
            int: Max digit number

        Raises:
            InvalidDigitsFormat: If digit is not supported regex format.
        """
        try:
            if re.match(r"^\d*,?\d*$", digits):
                return max(map(int, (digits.split(","))))
            else:
                raise InvalidDigitsFormat()
        except TypeError:
            raise InvalidDigitsFormat()

    @staticmethod
    def _rename_file(old_name, new_name):
        """Rename filename.

        Args:
            old_name (str): Old filename
            new_name (str): New filename

        Returns:
            bool: If success, return true.

        Raises:
            ChangeFileNameOSError: If rename failed.
        """
        try:
            os.rename(old_name, new_name)
            logger.info("Rename file success: {old_name} => {new_name}".format(old_name=old_name,
                                                                               new_name=new_name))
            return True
        except OSError as e:
            logger.exception(e)
            raise ChangeFileNameOSError()

    @staticmethod
    def _remove_file(file, assume_yes=False):
        """Remove filename.

        Args:
            file (str): filename
            assume_yes (bool): If True, no verify the user.

        Returns:
            bool: If success, return true.
        """
        if assume_yes is True:
            pass
        else:
            logger.info("Remove file: {file_name} OK? (y/n)".format(file_name=file))
            flag = input()
            if flag in ("Y", "y"):
                pass
            else:
                logger.info("Nothing..")
                return False
        os.remove(file)
        logger.info("Remove file success: {file_name}".format(file_name=file))
        return True

    def _move_file(self, file, dst, assume_yes=False):
        """Move file another directory

        Args:
            file (str): Target source file
            dst (str): Target destination directory or filename
            assume_yes (bool): If true, no verify the user

        Returns:
            bool: If success, return True.

        """
        dst_dir, _, _ = self._split_dir_root_ext(dst)
        if assume_yes is True:
            pass
        else:
            logger.info("Move file: {file_name} OK? (y/n/r)".format(file_name=file))
            flag = input()
            if flag == "Y" or flag == "y":
                pass
            else:
                logger.info("Nothing..")
                return False
        shutil.move(file, dst_dir)
        logger.info("Move file success: {file_name} => {dst_dir}".format(file_name=file, dst_dir=dst_dir))
        return True

    @staticmethod
    def _remove_file_bulk(file_list):
        """Remove files bulk.
        Args:
            file_list(List): File list

        Returns:
            bool: If success, return true.
        """
        if not file_list:
            return False
        for file in file_list:
            os.remove(file)
            logger.debug("Remove file: {file}".format(file=file))
        return True

    def _check_image_file(self, file_name):
        """Show image file.
        Args:
            file_name(str): Image file name

        Raises:
            InvalidImageParameterType: If you doesn't choose image file.
        """
        _, _, ext = self._split_dir_root_ext(file_name)
        if ext in (".jpg", ".png", ".gif"):
            draw_pic = PIL.Image.open(file_name)
            draw_pic.show()
        else:
            raise InvalidImageParameterType()
