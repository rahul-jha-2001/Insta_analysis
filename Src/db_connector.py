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
            self.myclient = pymongo.MongoClient(MONGO_DB)
            logging.info(f"DB connected at {MONGO_DB}")
        except Exception as e:
            raise CustomException(e)
    

    def push(self,data:json,db,document) -> None:
        collection = self.myclient[db][document]
        _ = collection.insert_one(data)
        logging.info(f"Data pushed into DB with following ids{_}")
    def pull(self,db:str,document:str,filter:dict,colunm:dict,limit:int = 0,sort:dict = None) -> list:
        if sort == None:
            return list(self.myclient[db][document].find(filter=filter,projection = colunm).limit(limit))
        elif sort != None:
            return list(self.myclient[db][document].find(filter=filter,projection = colunm).sort(sort).limit(limit))
            
    def push_many(self,data:list,db,document) -> None:
        collection = self.myclient[db][document]
        _ = collection.insert_many(data)
        logging.info(f"Data pushed into DB with following ids{_.inserted_ids}")
    def delete(self,db:str,document:str,filter:dict):
        collection = self.myclient[db][document]
        d = collection.delete_many(filter=filter)
        logging.info(f"{d.deleted_count} documents deleted")


