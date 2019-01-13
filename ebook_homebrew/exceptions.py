# -*- coding: utf-8 -*-
"""Exception Classes
"""


class BaseError(Exception):
    pass


class ChangeFileNameError(BaseError):
    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(error_class=self.error_class, message=self.message)


class MakePDFError(BaseError):
    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(error_class=self.error_class, message=self.message)


class MakeZIPError(BaseError):
    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(error_class=self.error_class, message=self.message)


class ZipFileExistError(MakeZIPError):
    def __init__(self):
        super().__init__("ZipFileExistError", "Already Zipfile you decide name exist. "
                                              "If overwrite, choose 'overwrite' parameter.")


class InvalidDigitsFormat(ChangeFileNameError):
    def __init__(self):
        super().__init__("ChangeFileNameError", "Invalid serial number digit value. "
                                                "If you want to use multiple digits, "
                                                "please divide into comma separator")


class InvalidExtensionType(ChangeFileNameError):
    def __init__(self):
        super().__init__("InvalidExtensionType", "Invalid Extension Type. "
                                                 "Expected string or bytes-like object")


class InvalidPathType(ChangeFileNameError):
    def __init__(self):
        super().__init__("InvalidPathType", "Invalid Path string Type. "
                                            "Expected string, bytes-like, os.Path-like object")


class TargetSrcFileNotFoundError(ChangeFileNameError):
    def __init__(self):
        super().__init__("TargetSrcFileNotFoundError", "Source directory you choose is no Target file.")


class InvalidNumberParameterType(ChangeFileNameError):
    def __init__(self):
        super().__init__("InvalidNumberParameterType", "To create new file name, must be used 'Integer'.")


class InvalidImageParameterType(ChangeFileNameError):
    def __init__(self):
        super().__init__("InvalidImageParameterType", "To check image file, "
                                                      "must be 'Image file' such as jpeg, png, or gif.")


class InvalidImageFileFormat(MakePDFError):
    def __init__(self):
        super().__init__("InvalidImageFileFormat", "Not supported file format. "
                                                   "Supported 'jpg', 'png', 'gif'")


class ChangeFileNameOSError(ChangeFileNameError):
    def __init__(self):
        super().__init__("ChangeFileNameOSError", "OSError was occurred. Reading more message above.")
