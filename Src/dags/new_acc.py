import sys
sys.path.append("/opt/Src")
print(sys.path)
from data_processor import ETL
from Scrape import Scrape
from datetime import datetime
from airflow import DAG
from airflow.decorators import task,dag

@task()
def Get():
    S = Scrape()
    S.run()
@task()
def Process():
    E = ETL()
    E.ETL()    

with DAG("New_Accounts","Workflow to get new accs",schedule_interval="*/10 * * * *",start_date=datetime(2024,6,12)) as dag:
    Get() >> Process()