from app import ModelBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, PickleType, JSON, Float, ARRAY, func, Table
from sqlalchemy.orm import relationship
from json import dumps

class ModelDatafileAssociation(ModelBase):
    __tablename__ = "model_datafile_associations",
    model_id = Column(ForeignKey("models.id"), primary_key = True)
    datafile_id = Column(ForeignKey("datafiles.id"), primary_key = True)
    role = Column(String)
    model = relationship("Model", back_populates = "datafiles")
    datafile = relationship("Datafile", back_populates = "models")
   
class Model(ModelBase):
    __tablename__ = "models"

    id = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable = False)
    dataset = relationship("Dataset", back_populates = "models")
    name = Column(String, nullable = False)
    is_public = Column(Boolean, nullable = False)
    notes = Column(String)
    class_name = Column(String, nullable = False)
    params = Column(JSON, nullable = False)
    target_name = Column(String, nullable = False)
    feature_names = Column(ARRAY(String), nullable = False)
    saved_model = Column(PickleType, nullable = False)
    fit_at = Column(DateTime(timezone = True))
    fit_time_ms = Column(Integer, nullable = False, default = 0)
    train_score = Column(Float, nullable = False, default = 0)
    val_score = Column(Float, nullable = False, default = 0)
    other_scores = Column(JSON, nullable = False, default = {})
    created_by = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())
    datafiles = relationship("ModelDatafileAssociation", back_populates = "model")

    def serialize(self):
        return {
            "id": self.id,
            "dataset_id": self.dataset_id,
            "dataset_name": self.dataset.name,
            "name": self.name,
            "is_public": self.is_public,
            "notes": self.notes,
            "datafiles": [{'datafile_id': file.datafile_id, 'role': file.role} for file in self.datafiles],
            "class_name": self.class_name,
            "params": dumps(self.params),
            "target_name": self.target_name,
            "feature_names": self.feature_names,
            "fit_at": str(self.fit_at),
            "train_score": self.train_score,
            "val_score": self.val_score,
            "created_by": self.created_by,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }