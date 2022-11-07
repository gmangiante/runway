from app import ModelBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, LargeBinary, func
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Dataset(ModelBase):
    __tablename__ = "datasets"

    id: int = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    name: str = Column(String, nullable = False)
    is_public: bool = Column(Boolean, nullable = False)
    created_by: str = Column(String, nullable = False)
    created_at: datetime = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at: datetime = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())

class Datafile(ModelBase):
    __tablename__ = "datafiles"

    id = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable = False)
    name = Column(String, nullable = False)
    content_type = Column(String, nullable = False)
    content = Column(LargeBinary, nullable = False)
    created_by = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())
    