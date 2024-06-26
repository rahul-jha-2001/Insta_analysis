import logging 
import os
import datetime

LOG_FILE = f'{datetime.datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.log'
LOG_PATH = "/tmp/Logs"
os.makedirs(LOG_PATH,exist_ok= True)

LOG_FILE_PATH = os.path.join(LOG_PATH,LOG_FILE)

logging.basicConfig(
    filename= LOG_FILE_PATH,
    force="[ %(asctime)s] %(linemo)d %(name)s - %(levelname)s - %(message)s",
    level= logging.DEBUG 
)
