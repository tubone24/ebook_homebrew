"""Provides Upload status models
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()


class UploadedFilesModel(Base):
    """Create Uploaded Files Model
    """

    __tablename__ = "uploaded_files"

    id = Column("id", INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column("name", String(64), index=True)
    file_path = Column("file_path", String(255), index=True, unique=True)
    file_type = Column("file_type", String(64))
    last_index = Column("last_index", INTEGER(unsigned=True), nullable=False)
    created_at = Column(
        "created_at",
        DateTime,
        default=datetime.now(),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )
