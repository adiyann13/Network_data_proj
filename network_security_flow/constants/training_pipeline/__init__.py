import os
import sys
import numpy as np
import pandas as pd

TRGET_COLUMN ='Result'
PIPELINE_NAME:str = "Network_security"
ARTIFACT_DIR:str = 'Artifacts'
FILE_NAME:str = 'Website Phishing.csv'

TRAIN_FILE_NAME:str = 'train.csv'
TEST_FILE_NAME:str = 'test.csv'

DATA_INGESTION_COLLECTION_NAME:str = 'Network_Data'
DATA_INDESTION_DATABASE_NAME:str = 'adiyannmd'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion_dir'
DATA_INGESTION_FEATURE_STORE_DATA :str = 'feature_store'
DATA_INGESTION_INGESTED_DATA:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2

DATA_SCHEMA_FILE_PATH:str = os.path.join('data_schema' , 'schema.yaml')

DATA_VALIDATION_DIR_NAME:str = 'data_validation'
DATA_VALIDATION_VALID_DIR:str  = 'validated_data'
DATA_VALIDATION_INVALID_DIR:str = 'invaled_data'
DATA_VALIDATION_DRIFT_REPORT:str = 'data_drift'
DATA_VALIDATION_FINAL_REPORT:str = 'report.yaml'

PRE_PROCESSING_FILE:str = 'preprocessing.pkl'


DATA_TRANSFORMATION_DIR_NAME:str = 'data_transformation'
DATA_TRANSFORMATION_TRANSOFRMED_DATA_DIR:str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = 'Ttransformed_object'

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict ={
    "missing_values": np.nan,
    'n_neighbors':3 , 
    'weights':'uniform',
}