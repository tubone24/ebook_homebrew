# -*- coding: utf-8 -*-
import os
import os.path
import re
import PIL
import PIL.Image
from utils.logging import get_logger
from utils.exceptions import InvalidDigitsFormat, InvalidNumberParameterType, \
    ChangeFileNameOSError, InvalidImageParameterType

logger = get_logger("change_filename")


class ChangeFilename(object):

    def __init__(self, directory_path, digits, extension):
        self.directory_path = directory_path
        self.digits = digits
        self.exist_files = []
        self.extension = self.__convert_extension_with_dot(extension)
        self.regex_ext = re.compile(self.extension)
        os.chdir(directory_path)

    @staticmethod
    def __convert_extension_with_dot(extension):
        if re.match(r"^\..+", extension):
            return extension
        else:
            return "." + extension

    @staticmethod
    def __split_dir_root_ext(path):
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)
        base_root, ext = os.path.splitext(base_name)
        return dir_name, base_root, ext

    @staticmethod
    def __check_serial_number(filename, digits):
        num = re.search("\\d{" + str(digits) + "}", filename)
        if num is None:
            return False, None
        return True, num

    @staticmethod
    def __check_digit_format(digits):
        if re.match(r"^\d*,?\d*$", digits):
            return max(map(int, (digits.split(","))))
        else:
            raise InvalidDigitsFormat()

    @staticmethod
    def __create_new_name(num, digit, extension):
        if type(num) is int:
            raise InvalidNumberParameterType()
        return num.group().zfill(digit) + extension

    @staticmethod
    def __rename_file(old_name, new_name):
        try:
            os.rename(old_name, new_name)
            logger.info("Rename file success: {old_name} => {new_name}".format(old_name=old_name,
                                                                               new_name=new_name))
            return True
        except OSError as e:
            logger.exception(e)
            raise ChangeFileNameOSError()

    @staticmethod
    def __remove_file(file):
        logger.info("Remove file: {file_name} OK? (y/n/r)".format(file_name=file))
        flag = input()
        if flag == "Y" or flag == "y":
            os.remove(file)
            logger.info("Remove file success: {file_name}".format(file_name=file))

    @staticmethod
    def __check_image_file(file_name):
        if file_name[:-4] == ".jpg" or ".png" or ".gif":
            draw_pic = PIL.Image.open(file_name)
            draw_pic.show()
        else:
            raise InvalidImageParameterType()

    def __check_exist_file(self, new_name, old_name, append_list):
        try:
            if os.path.isfile(new_name):
                logger.info("File Exist: {filename}".format(filename=new_name))
                if old_name != new_name and append_list:
                    logger.debug("Append exist files list: {filename}".format(filename=old_name))
                    self.exist_files.append(old_name)
                return True
            else:
                return False
        except OSError as e:
            logger.exception(e)
            raise ChangeFileNameOSError()

    def __input_new_file_name(self, old_name, overwrite):
        logger.info("Input new name? {old_name} =>".format(old_name=old_name))
        new_name = input()
        while self.__check_exist_file(new_name, None, False) and not overwrite:
            logger.warn("Already file exist: {new_name}   "
                        "Input Another file name {old_name} => ?".format(new_name=new_name,
                                                                         old_name=old_name))
            new_name = input()
        return new_name

    def filename_to_serial_number(self):
        count = 0
        files = os.listdir(self.directory_path)

        logger.info("Target directory: {directory_path}".format(directory_path=self.directory_path))
        logger.info("Digit: {digits}".format(digits=self.digits))
        logger.info("Extension: {extension}".format(extension=self.extension))
        logger.info("-" * 55)

        max_digit = self.__check_digit_format(self.digits)

        for file in files:
            is_num, num = self.__check_serial_number(file, self.digits)
            if not is_num:
                logger.debug("Skip(No number): {filename}".format(filename=str(file)))
            elif not self.regex_ext.search(file):
                logger.debug("Skip(No target extension): {filename}".format(filename=str(file)))
            else:
                new_name = self.__create_new_name(num, max_digit, self.extension)
                if not self.__check_exist_file(new_name, file, True):
                    self.__rename_file(file, new_name)
                    count += 1

        logger.info("-" * 55)
        logger.info("Finished! Rename file count: {count}".format(count=count))
        return self.exist_files

    def change_name_hand(self, overwrite):
        logger.info("-" * 55)
        logger.info("Manually determine file names duplicated by the serial number\n")
        for file in self.exist_files:
            logger.info("File name: {file_name} Does it rename? (y/n/r)".format(file_name=file))

            flag = input()
            if flag == "y" or flag == "Y":
                new_name = self.__input_new_file_name(file, overwrite)
                self.__rename_file(file, new_name)
                logger.info("Rename: {old_name} => {new_name} \n".format(old_name=file, new_name=new_name))
            elif flag == "r":
                logger.info("Will be {file} deleted?　OK? (y/n/c)".format(file=file))  # y="Yes" n="No" c="check"
                flag = input()
                if flag == "c":
                    try:
                        self.__check_image_file(file)
                    except InvalidImageParameterType as e:
                        logger.warn(e)
                        logger.info("Skip..")

                flag = input()
                if flag == "Y" or flag == "y":
                    self.__remove_file(file)
                elif flag == "r":
                    new_name = self.__input_new_file_name(file, overwrite)
                    self.__rename_file(file, new_name)
                else:
                    logger.info("Leave file: {file}\n".format(file=file))
            else:
                logger.info("Leave file: {file}\n".format(file=file))
        logger.info("Finished.")

    def add_str(self, before, after):
        logger.info("-" * 55)
        files = os.listdir(self.directory_path)
        if before is not None:
            logger.info("Add {before} before serial digit".format(before=before))
        else:
            before = ""
        if after is not None:
            logger.info("Add {after} before serial digit".format(after=after))
        else:
            after = ""

        for file in files:
            is_num, num = self.__check_serial_number(file, self.digits)
            if not is_num:
                logger.debug("Skip(No number): {filename}".format(filename=str(file)))
            else:
                if self.regex_ext.search(file):
                    _, center, _ = self.__split_dir_root_ext(file)
                    new_name = before + center + after + self.extension
                    if self.__check_exist_file(new_name, None, False):
                        pass
                    else:
                        self.__rename_file(file, new_name)
        return None


if __name__ == "__main__":
    obj = ChangeFilename("../tests", "3", "txt")
    obj.filename_to_serial_number()
    obj.change_name_hand(False)
    obj.add_str("before", "after")
