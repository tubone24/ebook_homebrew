"""Provides Rest API models
"""

import datetime


class StatusModel:
    """Status Model"""

    def __init__(self, status, version):
        self.status = status
        self.version = version


class UploadModel:
    """Upload_id Model"""

    def __init__(self, upload_id):
        self.upload_id = str(upload_id)
        self.release_date = datetime.datetime.now()


class ErrorModel:
    """Error Model"""

    def __init__(self, error):
        self.error = str(error)
        self.errorDate = datetime.datetime.now()


class FileNotFoundModel:
    """FileNotFound Model"""

    def __init__(self, reason):
        self.reason = reason
        self.errorDate = datetime.datetime.now()
