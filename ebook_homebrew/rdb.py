# -*- coding: utf-8 -*-
"""Provides RDB execute
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from .models.uploaded_files_models import Base, UploadedFilesModel

from .utils.logging import get_logger

_logger = get_logger("rdb")


class UploadedFile:
    """Provides UploadFile Sqlite3 operation
    """

    def __init__(self, dbname="ebook-homebrew.sqlite3", echo_log=True):
        """Constructor
        Create Sqlite3 db file and session.
        Args:
            dbname (str): Sqlite3 db name, default is ebook-homebrew.sqlite3
            echo_log (bool): If True, echo DB queries.
        """
        self.dbname = dbname
        self.engine = create_engine(
            "sqlite:///{dbname}".format(dbname=self.dbname), echo=echo_log
        )
        Base.metadata.create_all(self.engine)
        if not os.path.isfile(self.dbname):
            Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_uploaded_file(self, name, file_path, file_type, last_index):
        """Insert upload file

        Args:
            name (str): filename
            file_path (str): file path means upload ID
            file_type (str): ContentType like Image/png
            last_index (int): file index

        Returns:
            None: If Success
        Raises:
            SQLAlchemyError: SQL's Error
        """
        try:
            upload_files = UploadedFilesModel(
                name=name,
                file_path=file_path,
                file_type=file_type,
                last_index=last_index,
            )
            self.session.add(upload_files)
            self.session.commit()
        except SQLAlchemyError as err:
            _logger.exception(err)
            self.session.rollback()
            raise err
        except Exception as err:
            _logger.exception(err)
            self.session.rollback()
            raise err
        finally:
            self.session.close()

    def update_uploaded_file_last_index(self, table_id, last_index):
        """Update file last index.

        Args:
            table_id (str): id
            last_index (int): file last index

        Returns:
            None: If Success
        Raises:
            SQLAlchemyError: SQL's Error
        """
        try:
            query = self.session.query(UploadedFilesModel).with_lockmode("update")
            upload_file = query.filter(UploadedFilesModel.id == table_id).first()
            upload_file.last_index = last_index
            self.session.commit()
        except Exception as err:
            _logger.exception(err)
            self.session.rollback()
            raise err
        finally:
            self.session.close()

    def delete_uploaded_file(self, table_id):
        """Delete uploaded file with set id

        Args:
            table_id (str): id

        Returns:
            None: If Success
        Raises:
            SQLAlchemyError: SQL's Error
        """
        try:
            upload_file = (
                self.session.query(UploadedFilesModel)
                .filter(UploadedFilesModel.id == table_id)
                .first()
            )
            self.session.delete(upload_file)
            self.session.commit()
        except Exception as err:
            _logger.exception(err)
            self.session.rollback()
            raise err
        finally:
            self.session.close()

    def get_all_uploaded_file(self):
        """Get All uploaded files

        Returns:
            List[dict[int, str, str, str, int, datetime, datetime]]: uploaded files list
        Raises:
            SQLAlchemyError: SQL's Error
        """
        uploaded_file_list = []
        try:
            upload_files = self.session.query(UploadedFilesModel).all()
            for upload_file in upload_files:
                created_at = upload_file.created_at
                updated_at = upload_file.updated_at
                uploaded_file_list.append(
                    {
                        "id": upload_file.id,
                        "name": upload_file.name,
                        "file_path": upload_file.file_path,
                        "file_type": upload_file.file_type,
                        "last_index": upload_file.last_index,
                        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
            return uploaded_file_list
        except Exception as err:
            _logger.exception(err)
            raise err
        finally:
            self.session.close()

    def get_uploaded_file(self, table_id):
        """Get uploaded file

        Args:
            table_id (str): id

        Returns:
            dict[int, str, str, str, int, datetime, datetime]: uploaded file
        Raises:
            SQLAlchemyError: SQL's Error
        """
        try:
            upload_file = (
                self.session.query(UploadedFilesModel)
                .filter(UploadedFilesModel.id == table_id)
                .first()
            )
            if upload_file:
                created_at = upload_file.created_at
                updated_at = upload_file.updated_at
                upload_file_dict = {
                    "id": upload_file.id,
                    "name": upload_file.name,
                    "file_path": upload_file.file_path,
                    "file_type": upload_file.file_type,
                    "last_index": upload_file.last_index,
                    "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            else:
                upload_file_dict = {}
            return upload_file_dict
        except Exception as err:
            _logger.exception(err)
            raise err
        finally:
            self.session.close()
