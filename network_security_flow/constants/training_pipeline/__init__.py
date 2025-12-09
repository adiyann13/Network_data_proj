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