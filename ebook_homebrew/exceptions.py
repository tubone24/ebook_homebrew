# -*- coding: utf-8 -*-
"""Exception Classes
"""


class BaseError(Exception):
    """Base error
    """

    pass


class ChangeFileNameError(BaseError):
    """rename::ChangeFileName module error
    """

    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(
            error_class=self.error_class, message=self.message
        )


class MakePDFError(BaseError):
    """convert::MakePDF module error
    """

    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(
            error_class=self.error_class, message=self.message
        )


class MakeZIPError(BaseError):
    """archive::MakeZip module error
    """

    def __init__(self, error_class, message):
        self.error_class = error_class
        self.message = message

    def __str__(self):
        return "{error_class}: {message}".format(
            error_class=self.error_class, message=self.message
        )


class ZipFileExistError(MakeZIPError):
    """Zip file already exist error
    """

    def __init__(self):
        super().__init__(
            "ZipFileExistError",
            "Already Zipfile you decide name exist. "
            "If overwrite, choose 'overwrite' parameter.",
        )


class InvalidDigitsFormatError(ChangeFileNameError):
    """Invalid serial number digit value error
    """

    def __init__(self):
        super().__init__(
            "InvalidDigitsFormatError",
            "Invalid serial number digit value. "
            "If you want to use multiple digits, "
            "please divide into comma separator",
        )


class InvalidExtensionTypeError(ChangeFileNameError):
    """Invalid Extension Type error
    """

    def __init__(self):
        super().__init__(
            "InvalidExtensionTypeError",
            "Invalid Extension Type. " "Expected string or bytes-like object",
        )


class InvalidPathTypeError(ChangeFileNameError):
    """Invalid Path string Type error
    """

    def __init__(self):
        super().__init__(
            "InvalidPathTypeError",
            "Invalid Path string Type. "
            "Expected string, bytes-like, os.Path-like object",
        )


class TargetSrcFileNotFoundError(ChangeFileNameError):
    """Source directory you choose is no Target file error
    """

    def __init__(self):
        super().__init__(
            "TargetSrcFileNotFoundError",
            "Source directory you choose is no Target file.",
        )


class InvalidNumberParameterTypeError(ChangeFileNameError):
    """To create new file name, must be used 'Integer' error
    """

    def __init__(self):
        super().__init__(
            "InvalidNumberParameterTypeError",
            "To create new file name, must be used 'Integer'.",
        )


class InvalidImageParameterTypeError(ChangeFileNameError):
    """InvalidImageParameterTypeError
    """

    def __init__(self):
        super().__init__(
            "InvalidImageParameterTypeError",
            "To check image file, " "must be 'Image file' such as jpeg, png, or gif.",
        )


class InvalidImageFileFormatError(MakePDFError):
    """InvalidImageFileFormatError
    """

    def __init__(self):
        super().__init__(
            "InvalidImageFileFormatError",
            "Not supported file format." "Supported 'jpg', 'png', 'gif'",
        )


class ChangeFileNameOSError(ChangeFileNameError):
    """ChangeFileNameOSError
    """

    def __init__(self):
        super().__init__(
            "ChangeFileNameOSError", "OSError was occurred. Reading more message above."
        )
