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
    def __init__(self, dbname="ebook-homebrew.sqlite3", echo_log=True):
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

    def update_uploaded_file_last_index(self, id, last_index):
        try:
            query = self.session.query(UploadedFilesModel).with_lockmode("update")
            upload_file = query.filter(UploadedFilesModel.id == id).first()
            upload_file.last_index = last_index
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

    def delete_uploaded_file(self, id):
        try:
            upload_file = (
                self.session.query(UploadedFilesModel)
                .filter(UploadedFilesModel.id == id)
                .first()
            )
            self.session.delete(upload_file)
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

    def get_all_uploaded_file(self):
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
        except NoResultFound:
            _logger.warn("No Result found")
        except SQLAlchemyError as err:
            _logger.exception(err)
            raise err
        except Exception as err:
            _logger.exception(err)
            raise err
        finally:
            self.session.close()
            return uploaded_file_list

    def get_uploaded_file(self, id):
        try:
            upload_file = (
                self.session.query(UploadedFilesModel)
                .filter(UploadedFilesModel.id == id)
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
                return upload_file_dict
        except NoResultFound:
            _logger.warn("No Result found")
        except SQLAlchemyError as err:
            _logger.exception(err)
            raise err
        except Exception as err:
            _logger.exception(err)
            raise err
        finally:
            self.session.close()
