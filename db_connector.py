from logger import logging
from Exception import CustomException
import pymongo
import json
from datetime import datetime
import os
from dotenv import load_dotenv

class DB():

    
    def __init__(self) -> None:
        load_dotenv()
        MONGO_DB =   os.getenv("MONGO_DB")    
        try:
            myclient = pymongo.MongoClient(MONGO_DB)
            logging.info(f"DB connected at {MONGO_DB}")
        except Exception as e:
            raise CustomException(e)
    

    def push(self,data:json,db,document) -> None:
        collection = self.myclient[db][document]
        _ = collection.insert_one(data)
        logging.info(f"Data pushed into DB with following ids{_}")
    def pull(self,filter:dict,colunm:dict,db:str,document:str) -> list:
        return list(self.myclient[db][document].find(filter=filter,projection = colunm))
    

    
