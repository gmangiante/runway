from app import ModelBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, LargeBinary, func

class DatasetVisualization(ModelBase):
    __tablename__ = "datasetvisualizations"

    id = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable = False)
    name = Column(String, nullable = False)
    is_public = Column(Boolean, nullable = False)
    content_type = Column(String, nullable = False)
    content = Column(LargeBinary, nullable = False)
    created_by = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())

class ModelVisualization(ModelBase):
    __tablename__ = "modelvisualizations"

    id = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable = False)
    name = Column(String, nullable = False)
    is_public = Column(Boolean, nullable = False)
    content_type = Column(String, nullable = False)
    content = Column(LargeBinary, nullable = False)
    created_by = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())