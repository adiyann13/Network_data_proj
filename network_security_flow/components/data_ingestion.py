from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.entity.config_entity import DataIngestionConfig
from network_security_flow.entity.artifact_entity import DataIngestionArtifacts
import os
import sys
import pymongo
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_URI')


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
             raise NetwrokExceptions(e,sys)
    
    def export_mongo_data(self):
        try:
            db_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[db_name][collection_name]

            data = pd.DataFrame(list(collection.find()))

            for cls in data.columns:
                if cls == '_id':
                    data.drop(['_id'], axis=1, inplace=True)
            data.replace({'na':np.nan}, inplace=True)
            return data
        except Exception as e:
            raise NetwrokExceptions(e, sys)
        
   
        
    def store_raw_data(self, df:pd.DataFrame):
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            # write DataFrame to feature store and return the dataframe for downstream use
            df.to_csv(feature_store_path , index=False,header=True)
            return df
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def train_test_splitting(self,df:pd.DataFrame):
        try:
            training, testing = train_test_split(df , test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("perfoemed train test split")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("expoerting the train test file path")
            training.to_csv(self.data_ingestion_config.training_file_path, index = False , header=True)
            testing.to_csv(self.data_ingestion_config.testing_file_path , index = False , header = True)
        except Exception as e:
            raise NetwrokExceptions(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe =  self.export_mongo_data()
            dataframe = self.store_raw_data(dataframe)
            self.train_test_splitting(dataframe)
            dataingestartifact = DataIngestionArtifacts(training_file_path=self.data_ingestion_config.training_file_path,
                                                         testing_file_path= self.data_ingestion_config.testing_file_path)
            return dataingestartifact
        except Exception as e:
            raise NetwrokExceptions(e, sys)
        
    

