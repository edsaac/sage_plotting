import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sage_data_client
import streamlit as st
from datetime import datetime, date, time
from appmisc import *

with open("./assets/style.css") as f:
    st.markdown(f"""
        <style>{f.read()}</style>
        """, unsafe_allow_html=True)

"# 📈 Plot data from a SAGE node"
container = st.container()

with st.sidebar:
    st.image("https://portal.sagecontinuum.org/wsn-closed.dfca4c4b.png")
    with st.form("Form"):
        
        "## ⚙️ Parameter:"
        parameter = st.selectbox(
            "Parameter", 
            ["temperature", "relative_humidity", "pressure"],
            format_func=lambda x:x.title().replace("_"," "),
            label_visibility="collapsed")
        
        "## 📍 Node:"
        node_id = st.selectbox("Node", ["W083", "W024"], label_visibility="collapsed")

        "## 🗓️ Time range:"
        
        date_range = st.date_input(
            "Dates range",
            [date(2023, 2, 8), date(2023, 3, 1)],
            label_visibility="collapsed")
        
        start_date, end_date = date_range
        
        cols = st.columns(2)
        with cols[0]: start_time = st.time_input("Start time", time(0,0,0))
        with cols[1]: end_time = st.time_input("End time", time(0,0,0))

        iso_start_time = to_isodate(start_date, start_time)
        iso_end_time = to_isodate(end_date, end_time)
        
        # Retrieve data
        submit_button = st.form_submit_button(
            "Retrive data and plot", 
            use_container_width=True,
            type="primary")
            
with container:
    if submit_button:
        df = get_data(
            parameter,
            node_id,
            iso_start_time.isoformat(), 
            iso_end_time.isoformat())
        
        st.session_state.df = df

        st.plotly_chart(
            create_plotly_figure(df, node_id=node_id, parameter=parameter),
            use_container_width=True
        )

        with st.expander("Get matplotlib plot"):
            st.pyplot(create_matplotlib_figure(df, node_id=node_id, parameter=parameter))
    
    else:
        st.info(" 👈 Select options from the sidebar")