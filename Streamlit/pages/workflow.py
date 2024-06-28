import streamlit as st
import requests as rs
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv
load_dotenv()
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
st.set_page_config(page_title="Creator Dictionary",layout= "wide")
st.title("WorkFlow  Page")

def get_pause_stat(dag_id:str):
    return rs.get(url=f"http://10.10.10.2:8080/api/v1/dags/{dag_id}",auth = HTTPBasicAuth(USERNAME, PASSWORD)).json()["is_paused"]



def patch(dag_id:str,is_pause:bool):
    data_dag = rs.get(url=f"http://10.10.10.2:8080/api/v1/dags/{dag_id}",auth = HTTPBasicAuth(USERNAME, PASSWORD)).json()
    data_dag["is_paused"] = is_pause 
    rs.patch(url=f"http://10.10.10.2:8080/api/v1/dags/{dag_id}?update_mask=is_paused",
             headers= {"accept": "application/json" ,'Content-Type': 'application/json'},
             auth = HTTPBasicAuth(USERNAME,PASSWORD), 
                data = json.dumps({"is_paused":is_pause}))
    



def main(dag_id:str):
    st.write(f"Status of {dag_id}")
    curr_stat_new = get_pause_stat(dag_id)
    if curr_stat_new:
        st.write("Is PAUSED")
    else:
        st.write("Is ACTIVE")   


Top = st.columns(2)
with Top[0]:
    main("Monitor_Accounts")
    st.button(label="Activate",on_click=patch,args=("Monitor_Accounts",False),key="monitor_activate")
    st.button(label="deactivate",on_click=patch,args=("Monitor_Accounts",True),key="monitor_deactivate")

with Top[1]:  
    main("New_Accounts")          
    st.button(label="Activate",on_click=patch,args=("New_Accounts",False),key="new_activate")
    st.button(label="deactivate",on_click=patch,args=("New_Accounts",True),key="new_deactivate")