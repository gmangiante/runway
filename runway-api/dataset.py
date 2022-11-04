from __future__ import annotations
import pandas as pd
from os.path import exists, join
from os import mkdir
from flask import Blueprint, request, current_app, jsonify
from flask_cors import cross_origin, CORS
from auth import requires_auth
from werkzeug.utils import secure_filename
from uuid import uuid4
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Session = sessionmaker()

class Dataset(Base):
    __tablename__ = "datasets"
    columns = []
    predictors = []
    target = ''
    coeff = []
    train_score = 0
    test_score = 0
    db_repr = ''
    id = Column(String, primary_key = True)
    name = Column(String)
    filepath = Column(String)

    def __init__(self, id, name, filepath) -> None:
        self.id = str(id)
        self.name = name
        self.filepath = filepath

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "filepath": self.filepath,
            "columns": [{"name": index, "dtype": str(dtype) } for index, dtype in self.columns.items()],
            "target": self.target,
            "predictors": self.predictors,
            "coeff": [{"predictor": pred, "value": self.coeff[i]} for i, pred in enumerate(self.predictors)],
            "train_score": self.train_score,
            "test_score": self.test_score,
            "db_repr": self.db_repr
        }

    def __repr__(self):
        return "<Dataset(id='%s', name='%s', filepath='%s')>" % (
            self.id,
            self.name,
            self.filepath
        )

    @staticmethod
    def load_from_csv(dataset_id, filepath) -> Dataset:
        if not exists(filepath):
            raise Exception(f'File {filepath} not found')
        
        ds = Dataset(dataset_id, 'testname', filepath)
        df = pd.read_csv(filepath)
        ds.columns = df.dtypes
        ds.target = 'demand'
        ds.predictors = [col for col in df.drop(columns = ds.target)]
        lr = LinearRegression()
        X = df[ds.predictors]
        y = df[ds.target]
        X_train, X_val, y_train, y_val = train_test_split(X, y)
        lr.fit(X_train, y_train)
        ds.coeff = lr.coef_
        ds.train_score = lr.score(X_train, y_train)
        ds.test_score = lr.score(X_val, y_val)
        engine = create_engine("sqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
        session = Session()
        session.add(ds)
        this_ds = session.query(Dataset).filter_by(id = str(dataset_id)).first()
        ds.db_repr = this_ds.__repr__()
        return ds

dataset_api = Blueprint('dataset_api', __name__)
CORS(dataset_api, expose_headers=["Content-Type", "Authorization"], origins=['http://localhost:5173'])

@dataset_api.route("/upload", methods = ['POST'])
@requires_auth
def upload_file():
    dataset_id = uuid4()
    dataset_dir = join(current_app.root_path, 'datasets', str(dataset_id))
    mkdir(dataset_dir)
    f = request.files['file']
    dataset_file = join(dataset_dir, secure_filename(f.filename))
    f.save(dataset_file)
    ds = Dataset.load_from_csv(dataset_id, dataset_file)
    return jsonify(ds.serialize())