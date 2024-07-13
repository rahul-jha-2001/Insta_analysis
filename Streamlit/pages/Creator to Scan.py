import sys
sys.path.insert(0, '..')
from utils.db_connector import DB
import pandas as pd
import plotly as pl
import streamlit as st

def Add(username:str,Monitor:bool):
    if Monitor:
        D.push({"id":username,"priority":1},"Clean","To_scan")
    elif not Monitor:
        D.push({"id":username,"priority":3},"Clean","To_scan")

def remove(username:str,Monitor:bool):
    if Monitor:
        D.delete(filter={"id":username,"priority":1},db="Clean",document="To_scan")
    elif not Monitor:
        D.delete(filter={"id":username,"priority":3},db="Clean",document="To_scan")

def Clear(Monitor:bool):
    if Monitor:
        D.delete(filter={"priority":1},db="Clean",document="To_scan")
    elif not Monitor:
        D.delete(filter={"priority":3},db="Clean",document="To_scan")
def split_frame(input_df, rows):
        df = [input_df.iloc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
        return df




D = DB()
st.set_page_config(page_title="Current List",layout= "wide")



top_menu = st.columns(1)

with top_menu[0]:
    Priority = st.radio("New/Monitor", options=["New", "Monitor"], horizontal=1, index=1)
    if Priority == "New":
        df = pd.DataFrame(D.pull("Clean","To_scan",{"priority":3},{}))
    elif Priority == "Monitor":
        df = pd.DataFrame(D.pull("Clean","To_scan",{"priority":1},{}))


pagination = st.container()

bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[25, 50, 100])
with bottom_menu[1]:
    total_pages = (
        int(len(df) / batch_size) if int(len(df) / batch_size) > 0 else 1
    )
    current_page = st.number_input(
        "Page", min_value=1, max_value=total_pages, step=1
    )
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** ")
try:
    pages = split_frame(df, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
except IndexError:
    pass

bottom_menu_2 = st.columns(1)
with bottom_menu_2[0]:
    username = st.text_input(label="Enter username to Add/remove")
    monitor = st.radio("Monitor", options=[True, False], horizontal=1, index=1)


bottom_menu_3 = st.columns(3)
with bottom_menu_3[0]:
    Add_button = st.button("ADD")
    if Add_button:
        Add(username,Monitor=monitor)

with bottom_menu_3[1]:
    
    remove_button = st.button("Remove")
    if remove_button:
        remove(username,Monitor=monitor)

with bottom_menu_3[2]:
    
    Clear_button = st.button("Clear")
    if Clear_button:
        Clear(Monitor=monitor)
  