import sys
import os
import certifi
import pymongo
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.pipeline.training_pipeline import TrainingPipeline
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from network_security_flow.utils.ml_utils.models.estimator import NetworkModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_url = os.getenv("MONGO_URI")
print(mongo_url)


from network_security_flow.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_url, tlsCAFile = ca)

from network_security_flow.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from network_security_flow.constants.training_pipeline import DATA_INDESTION_DATABASE_NAME

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/",tags = ['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("training is done")
    except Exception as e:
        raise NetwrokExceptions(e,sys)

@app.post('/predict')
async def prediction(request:Request , file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        # Drop the target column if present
        if 'Result' in df.columns:
            df = df.drop(columns=['Result'])
        preprocessor = load_object('final_model/preprocessor.pkl')
        final_model = load_object('final_model/model.pkl')
        network_mod = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_mod.predict(df)
        df['predicted_data'] = y_pred
        df.to_csv('predicted_data/output_data.csv')
        values = df['predicted_data']
        return values
    except Exception as e:
        raise NetwrokExceptions(e,sys)

if __name__ == "__main__":
    app_run(app,host = 'localhost', port =8000)