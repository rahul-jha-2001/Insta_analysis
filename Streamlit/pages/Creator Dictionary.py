import sys
sys.path.insert(0, '..')
from utils.db_connector import DB
import pandas as pd
import plotly as pl
import streamlit as st


st.set_page_config(page_title="Creator Dictionary",layout= "wide")
Labels_required = ["username","verified","businessCategoryName","followersCount","postsCount","avg_reach","avg_ER","avg_likes","avg_cmnt","hashtags"]
@st.cache_data(show_spinner=False)
def Most_recent(df):
    Most_recent = []
    for i in df["username"].unique():
        date = max(df[df["username"] == i]["Date"])
        id = df[(df["username"] == i)]
        
        Most_recent.append(id[id["Date"] == date].index[0])
    df = df.iloc[Most_recent]
    return df[Labels_required]
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.iloc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df
def slider(df,name_of_column,coluumn,step = None) :
    with coluumn:
        try:
            ma,mi = max(df[name_of_column]),min((df[name_of_column]))
           
            range = st.slider(label=f"{name_of_column} Range",min_value = mi,max_value=ma,step=step)
            return df[df[name_of_column]<=range].copy()
        except:
            return df


D = DB()

df = pd.DataFrame(D.pull("Clean","Creators",{},{"_id":0}))
df = Most_recent(df)

head_menu = st.columns(3)
with head_menu[0]:
    sub_head =st.columns(2)
    with sub_head[0]:
        df = df[df["followersCount"] >= st.number_input("Greater Than",min_value=10000)]
    with sub_head[1]:
        df = df[df["followersCount"] <= st.number_input("Less Than",max_value=max(df["followersCount"]))]

df = slider(df,"avg_ER",head_menu[1])
df = slider(df,"avg_reach",head_menu[2])

#st.table(df)
top_menu = st.columns(3)
with top_menu[0]:
    sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
if sort == "Yes":
    with top_menu[1]:
        sort_field = st.selectbox("Sort By", options=df.columns)
    with top_menu[2]:
        sort_direction = st.radio(
            "Direction", options=["⬆️", "⬇️"], horizontal=True
        )
    df = df.sort_values(
        by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
    )
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


