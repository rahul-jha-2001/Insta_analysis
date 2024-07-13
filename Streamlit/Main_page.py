import streamlit as st 

st.set_page_config("Main Page",)

st.title("Main Page")
st.sidebar.success("Select From Above Pages")

st.write("""Welcome to CreatorInsight

CreatorInsight is your comprehensive tool for managing and analyzing creator data. This application provides a centralized platform to track, analyze, and manage information about content creators across various platforms.

Our application consists of five main components:

1. Creator Dictionary: Browse our extensive database of creators. This page displays a table with creator names and key statistics, giving you a quick overview of our tracked creators.

2. Creator Detail: Dive deep into individual creator profiles. Select a specific creator to view detailed information, including performance metrics, content analysis, and historical data.

3. Creator to Scan: View and manage the list of creators scheduled for data collection and analysis. This page helps you keep track of which creators are in the pipeline for updates.

4. Workflow: Monitor and control the status of ongoing data collection and analysis processes. This page provides real-time updates on various workflows and allows you to manage these processes efficiently.

5. Main Page (You are here): Your central hub for navigating the application and accessing key information at a glance.

Use the navigation menu to explore these different sections and unlock valuable insights about content creators in your network.

Get started by selecting one of the options above!""")