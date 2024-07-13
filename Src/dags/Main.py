import sys
sys.path.append("/opt/Src")
from data_processor import ETL
from Scrape import Scrape
from datetime import datetime
from airflow import DAG
from airflow.decorators import task,dag

@task()
def Get(Monitor_accs = False):
    S = Scrape()
    S.run(Monitor_accs)
@task()
def Process():
    E = ETL()
    E.ETL()    

with DAG("New_Accounts","Workflow to get new accs",schedule_interval="*/5 * * * *",start_date=datetime(2024, 1, 1),catchup=False) as dag:
    Get() >> Process()
with DAG("Monitor_Accounts","Workflow to get Monitor accs",schedule_interval="0 */24 * * *",start_date=datetime(2024, 1, 1),catchup=False) as dag2:
    Get(True) >> Process()
    