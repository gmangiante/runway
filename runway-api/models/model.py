from app import ModelBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, PickleType, JSON, Float, ARRAY, func
   
class Model(ModelBase):
    __tablename__ = "models"

    id = Column(Integer, primary_key = True, autoincrement = "auto", nullable = False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable = False)
    name = Column(String, nullable = False)
    is_public = Column(Boolean, nullable = False)
    class_name = Column(String, nullable = False)
    params = Column(JSON, nullable = False)
    target_name = Column(String, nullable = False)
    feature_names = Column(ARRAY(String), nullable = False)
    saved_model = Column(PickleType, nullable = False)
    fit_time_ms = Column(Integer, nullable = False, default = 0)
    train_score = Column(Float, nullable = False, default = 0)
    val_score = Column(Float, nullable = False, default = 0)
    other_scores = Column(JSON, nullable = False, default = {})
    created_by = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(DateTime(timezone = True), nullable = False, server_default = func.now(), onupdate = func.now())