
import sys
sys.path.insert(0, '..')
from utils.db_connector import DB
import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data(show_spinner=False)
def Most_recent(df):
    Most_recent = []
    for i in df["media_id"].unique():
        _id = max(df[df["media_id"] == i]["_id"])
        id = df[(df["media_id"] == i)]
        
        Most_recent.append(id[id["_id"] == _id].index[0])
    return df.iloc[Most_recent]


@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.iloc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df




D = DB()

st.set_page_config(page_title="Creator Insights",layout= "wide")
required_labels = ["type","caption","hashtags","timestamp","followersCount","ER_per","Reach_per","Likes_per","Cmnts_per",]


menu_1 =st.columns(1)
with menu_1[0]:
    Name =  st.text_input("Username",help= "Enter the Username of Creator,leaving this Blank will not present any data.")
Creator_data = D.pull("Clean","Creators",{"username":Name},{"_id":0})
Creator_df = pd.DataFrame(Creator_data)
if  Creator_data != []:
    data = D.pull("Clean","Posts",{"ownerId":Creator_data[0]["id"]},{})
    df = pd.DataFrame(data)
    flag =True
else:
    flag = False

if flag:


        
    df = Most_recent(df)[required_labels]
    

    df = df.sort_values(by=['timestamp'], ascending=False)
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
    menu_2 = st.columns(2)
    with menu_2[0]:
        st.text("Enagement Ratio of Posts \n over a timeperiod",)
        st.plotly_chart(px.line(df,y =df["ER_per"],x="timestamp"),)
        
    with menu_2[1]:
        st.text("Reach of Posts over a timeperiod",)
        st.plotly_chart(px.line(y = df["Reach_per"],x=df["timestamp"],labels=["Reach","Timestamp"]))
    menu_3 = st.columns(3)
    with menu_3[0]:
        st.text("Follower count of the Creator  \n over a timeperiod",)
        st.plotly_chart(px.line(y=Creator_df["followersCount"],x=Creator_df["Date"]))
    with menu_3[1]:
        st.text("Avg ER of the Creator \n over a timeperiod",)
        st.plotly_chart(px.line(y=Creator_df["avg_ER"],x=Creator_df["Date"]))
    with menu_3[2]:
        st.text("Avg Reach of the Creator \n over a timeperiod",)
        st.plotly_chart(px.line(y=Creator_df["avg_reach"].sort_values(),x=Creator_df["Date"]))    


