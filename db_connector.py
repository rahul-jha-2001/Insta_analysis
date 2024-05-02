from logger import logging
import sys
from Exception import CustomException
import pandas as pd
import pymongo
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
MONGO_DB =   os.getenv("MONGO_DB")
try:
    myclient = pymongo.MongoClient(MONGO_DB)
    logging.info(f"DB connected at {MONGO_DB}")
except Exception as e:
    raise CustomException(e)
    

def push(data:json,db,document) -> None:
    collection = myclient[db][document]
    _ = collection.insert_one(data)
    logging.info(f"Data pushed into DB with following ids{_}")
def pull(filter:dict,colunm:dict,db:str,document:str) -> list:
    return list(myclient[db][document].find(filter=filter,projection = colunm))
    


    
    
