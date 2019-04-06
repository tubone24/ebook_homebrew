# -*- coding: utf-8 -*-
"""Rename file name.
"""
import os
import os.path
import re

from .core import Common
from .exceptions import (
    InvalidNumberParameterTypeError,
    ChangeFileNameOSError,
    InvalidImageParameterTypeError,
)
from .utils.logging import get_logger

_logger = get_logger("change_filename")


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
        self.__max_digit = self._check_digit_format(self.__digits)
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
            InvalidNumberParameterTypeError: If input digit is not Match object.

        """
        try:
            return num.group().zfill(digit) + extension
        except AttributeError as attribute_error:
            _logger.exception(attribute_error)
            raise InvalidNumberParameterTypeError() from attribute_error

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
                _logger.info("File Exist: {filename}".format(filename=new_name))
                if old_name != new_name and append_list:
                    _logger.debug(
                        "Append exist files list: {filename}".format(filename=old_name)
                    )
                    self.__exist_files.append(old_name)
                return True
            else:
                return False
        except OSError as os_error:
            _logger.exception(os_error)
            raise ChangeFileNameOSError() from os_error

    def __input_new_file_name(self, old_name, overwrite):
        """Provide input command prompt.
        Args:
            old_name (str): Old name
            overwrite (bool): If true, ignore exist file name.

        Returns:
            str: new file name.
        """
        new_name = input("Input new name? {old_name} =>".format(old_name=old_name))
        while self.__check_exist_file(new_name, new_name, False) and not overwrite:
            _logger.warn("Already file exist: {new_name}")
            new_name = input(
                "Input Another file name {old_name} => ?".format(old_name=old_name)
            )
        return new_name

    def filename_to_digit_number(self):
        """Change file name to only digit name.

        Change file name contains digit like "foo001bar.txt" to
        only digit file name like "001.txt".

        Returns:
            List[str]: Skipping files list by exists same name.
        """
        count = 0
        files = self._make_file_list(self.__directory_path)

        _logger.info(
            "Target directory: {directory_path}".format(
                directory_path=self.__directory_path
            )
        )
        _logger.info("Digit: {digits}".format(digits=self.__digits))
        _logger.info("Extension: {extension}".format(extension=self.__extension))
        _logger.info("-" * 55)

        for file in files:
            self._rename_digit_filename(file)
            count += 1

        _logger.info("-" * 55)
        _logger.info("Finished! Rename file count: {count}".format(count=count))
        return self.__exist_files

    def async_filename_to_digit_number(self):
        """Change file name to only digit name on async.

        If use this function, a little bit speedy
        compare with filename_to_digit_number function.

        Returns:
            List[str]: Skipping files list by exists same name.
        """
        files = self._make_file_list(self.__directory_path)

        _logger.info(
            "Target directory: {directory_path}".format(
                directory_path=self.__directory_path
            )
        )
        _logger.info("Digit: {digits}".format(digits=self.__digits))
        _logger.info("Extension: {extension}".format(extension=self.__extension))
        _logger.info("-" * 55)

        loop = self._get_eventloop()
        queue = self._create_task_queue(files)
        loop.run_until_complete(
            self._execute_queuing_tasks(queue, loop, None, self._rename_digit_filename)
        )
        _logger.info("-" * 55)
        _logger.info("Finished! Async rename")
        return self.__exist_files

    def _rename_digit_filename(self, file):
        num = self._check_serial_number(file, self.__digits)
        if not self._check_skip_file(file, self.__regex_ext, num):
            new_name = self._create_new_name(num, self.__max_digit, self.__extension)
            if not self.__check_exist_file(new_name, file, True):
                self._rename_file(file, new_name)
        return True

    def change_name_manually(self, overwrite=False):
        """Change filename manually looking exist_file list.

        After changing file name for filename_to_digit_number() method,
        duplicate file name change manually.

        Args:
            overwrite (bool): If true, overwrite file name even if exist same name file.

        Returns:
            bool: If success, return True.

        """

        def _flag_yes():
            new_name_y = self.__input_new_file_name(file, overwrite)
            self._rename_file(file, new_name_y)
            _logger.info(
                "Rename: {old_name} => {new_name} \n".format(
                    old_name=file, new_name=new_name_y
                )
            )

        def _flag_rename():
            flag_delete = input(
                "Will be {file} deleted? " "OK? (y/n/c/r)".format(file=file)
            )  # y="Yes" n="No" c="check" r="rename"
            if flag_delete == "c":
                self._check_image_file(file)
            elif flag_delete in ("Y", "y"):
                self._remove_file(file)
            elif flag_delete == "r":
                new_name_rename = self.__input_new_file_name(file, overwrite)
                self._rename_file(file, new_name_rename)
            else:
                _logger.info("Leave file: {file}\n".format(file=file))

        _logger.info("-" * 55)
        _logger.info("Manually determine file names duplicated by the serial number\n")
        for file in self.__exist_files:
            _logger.info("File name: {file_name}")
            flag = input(
                "Does it rename? (y/n/r)".format(file_name=file)
            )  # y="Yes" n="No" r="Remove"
            if flag in ("Y", "y"):
                _flag_yes()
            elif flag == "r":
                try:
                    _flag_rename()
                except InvalidImageParameterTypeError as invalid_image_parameter_type:
                    _logger.warn(invalid_image_parameter_type)
                    _logger.info("Skip..")
            else:
                _logger.info("Leave file: {file}\n".format(file=file))
        _logger.info("Finished.")
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
        _logger.info("-" * 55)
        files = self._make_file_list(self.__directory_path)
        if before is not None:
            _logger.info("Add {before} before serial digit".format(before=before))
        else:
            before = ""
        if after is not None:
            _logger.info("Add {after} before serial digit".format(after=after))
        else:
            after = ""

        for file in files:
            num = self._check_serial_number(file, self.__digits)
            if not num:
                _logger.debug("Skip(No number): {filename}".format(filename=str(file)))
            else:
                if self.__regex_ext.search(file):
                    _, center, _ = self._split_dir_root_ext(file)
                    new_name = before + center + after + self.__extension
                    if self.__check_exist_file(new_name, new_name, False):
                        pass
                    else:
                        self._rename_file(file, new_name)
        return True
