import os
from dotenv import load_dotenv
import json
import sys
import certifi
import pandas as pd
import numpy as np
import pymongo
from network_security_flow.logging import logger
from network_security_flow.exceptions import exception

load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
print(MONGO_URL)


ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise exception
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True , inplace = True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except exception as e:
            raise exception
        
    def insert_data_mongo(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records 
            self.mongo_client = pymongo.MongoClient(MONGO_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            print("not able to insert records")

if __name__ =='__main__':
    file_path = 'Netrwork_security_data\Website Phishing.csv'
    database = 'adiyannmd'
    collection = 'Network_Data'
    netwrokobj = NetworkDataExtract()
    converted_data = netwrokobj.csv_to_json(file_path=file_path)
    print(converted_data)
    no_of_records = netwrokobj.insert_data_mongo(converted_data,database,collection )
    print(no_of_records)