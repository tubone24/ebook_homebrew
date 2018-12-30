class BaseError(Exception):
    pass


class ChangeFileNameError(BaseError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return "{expression}: {message}".format(expression=self.expression, message=self.message)


class InvalidDigitsFormat(ChangeFileNameError):
    def __init__(self):
        self.expression = "ChangeFileNameError"
        self.message = "Invalid serial number digit value. " \
                       "If you want to use multiple digits, " \
                       "please divide into comma separator"


class InvalidNumberParameterType(ChangeFileNameError):
    def __init__(self):
        self.expression = "InvalidNumberParameterType"
        self.message = "To create new file name, must be used 'Integer'."


class InvalidImageParameterType(ChangeFileNameError):
    def __init__(self):
        self.expression = "InvalidImageParameterType"
        self.message = "To check image file, must be 'Image file' such as jpeg, png, or gif."


class ChangeFileNameOSError(ChangeFileNameError):
    def __init__(self):
        self.expression = "ChangeFileNameOSError"
        self.message = "OSError was occurred. Reading more message above."
