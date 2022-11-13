from app import ModelBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, LargeBinary, func
from sqlalchemy.orm import relationship
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
    files = relationship("Datafile", back_populates="dataset")
    models = relationship("Model", back_populates="dataset")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_public": self.is_public,
            "created_by": self.created_by,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "files": [file.serialize() for file in self.files],
            "models": [model.serialize() for model in self.models]
        }

class Datafile(ModelBase):
    __tablename__ = "datafiles"

    id = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable = False)
    dataset = relationship("Dataset", back_populates="files")
    name = Column(String, nullable = False)
    content_type = Column(String, nullable = False)
    content = Column(LargeBinary, nullable = False)
    created_by = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())
    models = relationship("ModelDatafileAssociation", back_populates = "datafile")
    
    def serialize(self):
        return {
            "id": self.id,
            "dataset_id": self.dataset_id,
            "name": self.name,
            "content_type": self.content_type,
            "created_by": self.created_by,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
    