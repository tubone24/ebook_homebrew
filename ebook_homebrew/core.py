# -*- coding: utf-8 -*-
"""Core module
"""
import os
import re
import shutil
import asyncio

import PIL.Image

from .exceptions import (
    InvalidDigitsFormatError,
    ChangeFileNameOSError,
    InvalidImageParameterTypeError,
    InvalidExtensionTypeError,
    InvalidPathTypeError,
    TargetSrcFileNotFoundError,
)
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
        except TypeError as type_error:
            raise InvalidExtensionTypeError() from type_error

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
        except (TypeError, AttributeError) as origin_error:
            raise InvalidPathTypeError() from origin_error

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
            InvalidDigitsFormatError: If digit is not supported regex format.
        """
        try:
            if re.match(r"^\d*,?\d*$", digits):
                return max(map(int, (digits.split(","))))
            else:
                raise InvalidDigitsFormatError()
        except TypeError as type_error:
            raise InvalidDigitsFormatError() from type_error

    @staticmethod
    def _check_skip_file(filename, regex_ext, num):
        """Check skip or target file for target extension and num regex
        Args:
            filename (str): Filename which check
            regex_ext (Match): Compile extension object
            num (Match): Number match object

        Returns:
            bool: If True, filename is skip file.
        """
        if not num:
            logger.debug("Skip(No number): {filename}".format(filename=filename))
            return True
        elif not regex_ext.search(filename):
            logger.debug(
                "Skip(No target extension): {filename}".format(filename=filename)
            )
            return True
        else:
            return False

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
            logger.info(
                "Rename file success: {old_name} => {new_name}".format(
                    old_name=old_name, new_name=new_name
                )
            )
            return True
        except OSError as os_error:
            logger.exception(os_error)
            raise ChangeFileNameOSError() from os_error

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
            flag = input("Remove file: {file_name} OK? (y/n)".format(file_name=file))
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
        if assume_yes is False:
            flag = input("Move file: {file_name} OK? (y/n/r)".format(file_name=file))
            if flag not in ("Y", "y"):
                logger.info("Nothing..")
                return False
        shutil.move(file, dst_dir)
        logger.info(
            "Move file success: {file_name} => {dst_dir}".format(
                file_name=file, dst_dir=dst_dir
            )
        )
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

    @staticmethod
    def _make_file_list(directory_path, sort=False):
        try:
            files = os.listdir(directory_path)
        except FileNotFoundError:
            raise TargetSrcFileNotFoundError()
        if sort:
            files.sort()
        return files

    def _check_image_file(self, file_name):
        """Show image file.
        Args:
            file_name(str): Image file name

        Raises:
            InvalidImageParameterTypeError: If you doesn't choose image file.
        """
        _, _, ext = self._split_dir_root_ext(file_name)
        if ext in (".jpg", ".png", ".gif"):
            draw_pic = PIL.Image.open(file_name)
            draw_pic.show()
        else:
            raise InvalidImageParameterTypeError()

    def move_file(self, file, dst, assume_yes):
        """Move file

        Args:
            file (str): Target file name
            dst (str): Target destination path
            assume_yes (bool): If true, no verify users

        Returns:
            bool: If success, return true. Nothing target, return false.

        """
        destination = os.path.join(dst, file)
        return self._move_file(file=file, dst=destination, assume_yes=assume_yes)

    @staticmethod
    def _get_eventloop():
        """Get event loop

        Returns:
            event_loop: Event loop object
        """
        loop = asyncio.get_event_loop()
        return loop

    @staticmethod
    def _output_result(future):
        """Output async queue task result

        Args:
            future: Async future

        Returns:
            bool: If success, return true.
        """
        logger.info(future.result())
        return True

    @staticmethod
    def _create_task_queue(task_list):
        """Make async queue and put tasks

        Returns:
            asyncio.Queue: Async task queue
        """
        queue = asyncio.Queue()

        for task in task_list:
            queue.put_nowait(task)

        return queue

    async def _set_task_queue_for_executor(self, queue, loop, executor, func):
        """Set task queue using executor

        Args:
            queue: asyncio queue
            loop: event loop
            executor: executor
            func: function

        Returns:
            future
        """
        while not queue.empty():
            task = await queue.get()
            future = loop.run_in_executor(executor, func, task)
            future.add_done_callback(self._output_result)
            await future

    async def _execute_queuing_tasks(self, queue, loop, executor, func):
        """Execute queue tasks"""
        tasks = [
            self._set_task_queue_for_executor(queue, loop, executor, func)
            for i in range(os.cpu_count())
        ]
        return await asyncio.wait(tasks)
