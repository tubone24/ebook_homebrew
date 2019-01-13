# -*- coding: utf-8 -*-
"""Rename file name.
"""
import os
import os.path
import re

from .core import Common
from .exceptions import InvalidNumberParameterType, \
    ChangeFileNameOSError, InvalidImageParameterType, TargetSrcFileNotFoundError
from .utils.logging import get_logger

logger = get_logger("change_filename")


class ChangeFilename(Common):
    """Change file name to only digit name.
    """

    def __init__(self, directory_path, digits, extension):
        """Constructor

        Args:
            directory_path (str): Target directory path.
            digits (str): Regex target digit.
            extension (str): Target file extension.
        """
        super().__init__()
        self.__directory_path = directory_path
        self.__digits = digits
        self.__exist_files = []
        self.__extension = self._convert_extension_with_dot(extension)
        self.__regex_ext = re.compile(self.__extension)
        os.chdir(self.__directory_path)

    @staticmethod
    def _create_new_name(num, digit, extension):
        """Create only digit file name.

        Args:
            num (Match): Match object
            digit (int): digit number
            extension (str): File Extension like ".jpg"

        Returns:
            str: Only digit file name.

        Raises:
            InvalidNumberParameterType: If input digit is not Match object.

        """
        try:
            return num.group().zfill(digit) + extension
        except AttributeError as e:
            logger.exception(e)
            raise InvalidNumberParameterType()

    def __check_exist_file(self, new_name, old_name, append_list):
        """Check current directory and exists same name file, return true.
        Args:
            new_name (str): Target file name.
            old_name (str): before name
            append_list (bool): If true, make duplicate name list

        Returns:
            bool: If success, return true

        Raises:
            ChangeFileNameOSError: If input a bad filename or path.
        """
        try:
            if os.path.isfile(new_name):
                logger.info("File Exist: {filename}".format(filename=new_name))
                if old_name != new_name and append_list:
                    logger.debug("Append exist files list: {filename}".format(filename=old_name))
                    self.__exist_files.append(old_name)
                return True
            else:
                return False
        except OSError as e:
            logger.exception(e)
            raise ChangeFileNameOSError()

    def __input_new_file_name(self, old_name, overwrite):
        """Provide input command prompt.
        Args:
            old_name (str): Old name
            overwrite (bool): If true, ignore exist file name.

        Returns:
            str: new file name.
        """
        logger.info("Input new name? {old_name} =>".format(old_name=old_name))
        new_name = input()
        while self.__check_exist_file(new_name, new_name, False) and not overwrite:
            logger.warn("Already file exist: {new_name}   "
                        "Input Another file name {old_name} => ?".format(new_name=new_name,
                                                                         old_name=old_name))
            new_name = input()
        return new_name

    def filename_to_digit_number(self):
        """Change file name to only digit name.

        Change file name contains digit like "foo001bar.txt" to
        only digit file name like "001.txt".

        Returns:
            List[str]: Skipping files list by exists same name.
        """
        count = 0
        try:
            files = os.listdir(self.__directory_path)
        except FileNotFoundError:
            raise TargetSrcFileNotFoundError()

        logger.info("Target directory: {directory_path}".format(directory_path=self.__directory_path))
        logger.info("Digit: {digits}".format(digits=self.__digits))
        logger.info("Extension: {extension}".format(extension=self.__extension))
        logger.info("-" * 55)

        max_digit = self._check_digit_format(self.__digits)

        for file in files:
            num = self._check_serial_number(file, self.__digits)
            if not num:
                logger.debug("Skip(No number): {filename}".format(filename=file))
            elif not self.__regex_ext.search(file):
                logger.debug("Skip(No target extension): {filename}".format(filename=file))
            else:
                new_name = self._create_new_name(num, max_digit, self.__extension)
                if not self.__check_exist_file(new_name, file, True):
                    self._rename_file(file, new_name)
                    count += 1

        logger.info("-" * 55)
        logger.info("Finished! Rename file count: {count}".format(count=count))
        return self.__exist_files

    def change_name_manually(self, overwrite=False):
        """Change filename manually looking exist_file list.

        After changing file name for filename_to_digit_number() method,
        duplicate file name change manually.

        Args:
            overwrite (bool): If true, overwrite file name even if exist same name file.

        Returns:
            bool: If success, return True.

        """
        logger.info("-" * 55)
        logger.info("Manually determine file names duplicated by the serial number\n")
        for file in self.__exist_files:
            logger.info("File name: {file_name} "
                        "Does it rename? (y/n/r)".format(file_name=file))  # y="Yes" n="No" r="Remove"

            flag = input()
            if flag == "y" or flag == "Y":
                new_name = self.__input_new_file_name(file, overwrite)
                self._rename_file(file, new_name)
                logger.info("Rename: {old_name} => {new_name} \n".format(old_name=file, new_name=new_name))
            elif flag == "r":
                logger.info("Will be {file} deleted?"
                            "　OK? (y/n/c/r)".format(file=file))  # y="Yes" n="No" c="check" r="rename"
                flag = input()
                if flag == "c":
                    try:
                        self._check_image_file(file)
                    except InvalidImageParameterType as e:
                        logger.warn(e)
                        logger.info("Skip..")

                if flag == "Y" or flag == "y":
                    self._remove_file(file)
                elif flag == "r":
                    new_name = self.__input_new_file_name(file, overwrite)
                    self._rename_file(file, new_name)
                else:
                    logger.info("Leave file: {file}\n".format(file=file))
            else:
                logger.info("Leave file: {file}\n".format(file=file))
        logger.info("Finished.")
        return True

    def add_before_after_str(self, before, after):
        """Add file name specify string.

        After changing file name for filename_to_digit_number() method,
        add specify string before or after file name.

        Args:
            before (str): String before file name
            after (str): String after file name

        Returns:
            bool: If success, return True.

        """
        logger.info("-" * 55)
        files = os.listdir(self.__directory_path)
        if before is not None:
            logger.info("Add {before} before serial digit".format(before=before))
        else:
            before = ""
        if after is not None:
            logger.info("Add {after} before serial digit".format(after=after))
        else:
            after = ""

        for file in files:
            num = self._check_serial_number(file, self.__digits)
            if not num:
                logger.debug("Skip(No number): {filename}".format(filename=str(file)))
            else:
                if self.__regex_ext.search(file):
                    _, center, _ = self._split_dir_root_ext(file)
                    new_name = before + center + after + self.__extension
                    if self.__check_exist_file(new_name, new_name, False):
                        pass
                    else:
                        self._rename_file(file, new_name)
        return True
