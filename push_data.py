# import os 
# import sys 
# import json

# from dotenv import load_dotenv

# load_dotenv()

# MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# print(MONGO_DB_URL)


import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

# trusted certificate authorities 
import certifi 
ca=certifi.where()


# read the data from CSV 

import pandas as pd 
import numpy as np 
import pymongo 
from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging 

class NetworkDataExtract():
    def __init__(self):
        try :
            pass

        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        

    def csv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)

            record = list(json.loads(data.T.to_json()).values())
            return record
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def insert_data_mongodb(self,record,database,collection):
        try :
            self.database = database 
            self.collection = collection
            self.record = record

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.db = self.mongo_client[self.database]

            self.collection = self.db[self.collection]
            self.collection.insert_many(self.record)

            return (len(self.record))
        except Exception as e:
            raise NetworkSecurityException(e,sys)



if __name__ == '__main__':


    FILE_PATH = 'Network_Data/phisingData.csv'
    DATABASE="MuditAI"
    Collection="NetworkData"
    networkobj = NetworkDataExtract()
    # print('hello')

    # # networkobj.csv_to_json_convertor(file_path=FILE_PATH)

    # record = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    # print(record)

    # no_of_records = networkobj.insert_data_mongodb(record=record,database=DATABASE,collection=Collection)

    # print(no_of_records)
    
    # # if __name__ == '__main__':
    logging.info("Starting the script...")
    try:
        networkobj = NetworkDataExtract()
        logging.info(f"Processing file: {FILE_PATH}")
        record = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(record)
        logging.info(f"Converted records: {len(record)}")
        no_of_records = networkobj.insert_data_mongodb(record=record, database=DATABASE, collection=Collection)
        logging.info(f"Number of records inserted: {no_of_records}")
        print(no_of_records)
    except NetworkSecurityException as e:
        logging.error(str(e))
        print(e)
