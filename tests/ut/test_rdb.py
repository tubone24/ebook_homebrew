import os
from datetime import datetime
import logging
from unittest.mock import patch
import pytest

from sqlalchemy.exc import SQLAlchemyError
from ebook_homebrew.rdb import UploadedFile


_logger = logging.getLogger(name=__name__)


class TestUploadFile(object):
    def setup_method(self, method):
        if os.path.exists("test-ebook-homebrew.sqlite3"):
            os.remove("test-ebook-homebrew.sqlite3")
        self.dbname = "test-ebook-homebrew.sqlite3"
        _logger.info("method{}".format(method.__name__))
        self.target = UploadedFile(dbname=self.dbname)

    def teardown_method(self, method):
        _logger.info("method{}".format(method.__name__))
        self.target.session.close()

    def test_init(self):
        assert os.path.exists(self.dbname)

    def test_ok_1_add_uploaded_file(self):
        self.target.add_uploaded_file("testfile", "/tmp/testfile", "image/png", 0)
        res = self.target.session.execute("SELECT * FROM uploaded_files")
        actual = []
        for v in res:
            actual.append({"id": v[0], "name": v[1], "file_path": v[2], "file_type": v[3], "last_index": v[4]})
        assert actual[0] == {"id": 1, "name": "testfile", "file_path": "/tmp/testfile", "file_type": "image/png", "last_index": 0}

    def test_ok_many_add_uploaded_file(self):
        self.target.add_uploaded_file("testfile", "/tmp/testfile", "image/png", 0)
        self.target.add_uploaded_file("testfile2", "/tmp/testfile2", "image/png", 1)
        res = self.target.session.execute("SELECT * FROM uploaded_files")
        actual = []
        for v in res:
            actual.append({"id": v[0], "name": v[1], "file_path": v[2], "file_type": v[3], "last_index": v[4]})
        assert actual[0] == {"id": 1, "name": "testfile", "file_path": "/tmp/testfile", "file_type": "image/png", "last_index": 0}
        assert actual[1] == {"id": 2, "name": "testfile2", "file_path": "/tmp/testfile2", "file_type": "image/png", "last_index": 1}

    def test_sql_alchemy_error_add_uploaded_file(self):
        with patch("ebook_homebrew.models.uploaded_files_models.UploadedFilesModel.__init__", side_effect=SQLAlchemyError):
            with pytest.raises(SQLAlchemyError):
                self.target.add_uploaded_file("testfile", "/tmp/testfile", "image/png", 0)

    def test_exception_add_uploaded_file(self):
        with patch("ebook_homebrew.models.uploaded_files_models.UploadedFilesModel.__init__", side_effect=Exception):
            with pytest.raises(Exception):
                self.target.add_uploaded_file("testfile", "/tmp/testfile", "image/png", 0)

    def test_ok_update_uploaded_file_last_index(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target.session.execute("INSERT INTO uploaded_files values(1, 'testfile', '/tmp/testfile', 'image/png', 0, '{now}', '{now}')".format(now=now))
        self.target.update_uploaded_file_last_index("1", 2)
        res = self.target.session.execute("SELECT * FROM uploaded_files")
        actual = []
        for v in res:
            actual.append({"id": v[0], "name": v[1], "file_path": v[2], "file_type": v[3], "last_index": v[4]})
        assert actual[0] == {"id": 1, "name": "testfile", "file_path": "/tmp/testfile", "file_type": "image/png", "last_index": 2}

    def test_exception_update_uploaded_file_last_index(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target.session.execute("INSERT INTO uploaded_files values(1, 'testfile', '/tmp/testfile', 'image/png', 0, '{now}', '{now}')".format(now=now))
        with patch("ebook_homebrew.models.uploaded_files_models.UploadedFilesModel.id", side_effect=Exception):
            with pytest.raises(Exception):
                self.target.update_uploaded_file_last_index("1", 2)

    def test_ok_delete_uploaded_file(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target.session.execute("INSERT INTO uploaded_files values(1, 'testfile', '/tmp/testfile', 'image/png', 0, '{now}', '{now}')".format(now=now))
        self.target.delete_uploaded_file("1")
        res = self.target.session.execute("SELECT * FROM uploaded_files")
        actual = []
        for v in res:
            actual.append({"id": v[0], "name": v[1], "file_path": v[2], "file_type": v[3], "last_index": v[4]})
        assert actual == []

    def test_sql_alchemy_error_delete_uploaded_file(self):
        with pytest.raises(SQLAlchemyError):
            self.target.delete_uploaded_file("1")

    def test_exception_delete_uploaded_file(self):
        with patch("ebook_homebrew.models.uploaded_files_models.UploadedFilesModel.id", return_value=Exception):
            with pytest.raises(Exception):
                self.target.delete_uploaded_file("1")

    def test_ok_get_all_uploaded_file(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target.session.execute("INSERT INTO uploaded_files values(1, 'testfile', '/tmp/testfile', 'image/png', 0, '{now}', '{now}')".format(now=now))
        self.target.session.execute("INSERT INTO uploaded_files values(2, 'testfile2', '/tmp/testfile2', 'image/png', 1, '{now}', '{now}')".format(now=now))
        actual = self.target.get_all_uploaded_file()
        expected = [
            {"id": 1, "name": "testfile", "file_path": "/tmp/testfile", "file_type": "image/png", "last_index": 0, "created_at": now, "updated_at": now},
            {"id": 2, "name": "testfile2", "file_path": "/tmp/testfile2", "file_type": "image/png", "last_index": 1, "created_at": now, "updated_at": now}
        ]
        assert actual == expected

    def test_ok_get_uploaded_file(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target.session.execute("INSERT INTO uploaded_files values(1, 'testfile', '/tmp/testfile', 'image/png', 0, '{now}', '{now}')".format(now=now))
        self.target.session.execute("INSERT INTO uploaded_files values(2, 'testfile2', '/tmp/testfile2', 'image/png', 1, '{now}', '{now}')".format(now=now))
        actual = self.target.get_uploaded_file("2")
        expected = {"id": 2, "name": "testfile2", "file_path": "/tmp/testfile2", "file_type": "image/png", "last_index": 1, "created_at": now, "updated_at": now}
        assert actual == expected

    def test_notfound_get_uploaded_file(self):
        actual = self.target.get_uploaded_file("2")
        expected = {}
        assert actual == expected


