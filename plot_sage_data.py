import pandas as pd
import matplotlib.pyplot as plt
import sage_data_client
import streamlit as st
from datetime import datetime, date

@st.cache_data()
def get_data(parameter:str, start_datetime:str, end_datetime:str):

    df = sage_data_client.query(
        start=start_datetime,
        end=end_datetime,
        filter={
            "name": f"env.{parameter}",
            "sensor": "bme680",
            "vsn":"W083",
        }
    )
    
    return df

"# 📈 Plot data from a SAGE node"
container = st.container()

with st.sidebar:
    with st.form("Form"):
        
        "## Parameter:"
        parameter = st.selectbox(
            "Select one", 
            ["temperature", "relative_humidity", "pressure"],
            format_func=lambda x:x.title().replace("_"," "))

        "## From:"
        cols = st.columns(2)
        with cols[0]: 
            start_date = st.date_input(
                "Start date",
                date(2023, 2, 8))
        
        with cols[1]: 
            start_time = st.time_input("Start time")
        
        iso_start_time = datetime(
            start_date.year, start_date.month, start_date.day,
            start_time.hour, start_time.minute, start_time.second)

        "## To:"
        cols = st.columns(2)
        with cols[0]: 
            end_date = st.date_input(
                "End date", 
                date(2023, 2, 10))
        
        with cols[1]: 
            end_time = st.time_input("End time")
        
        iso_end_time = datetime(
            end_date.year, end_date.month, end_date.day,
            end_time.hour, end_time.minute, end_time.second)
        
        # Retrieve data
        submit_button = st.form_submit_button(
            "Retrive data and plot", 
            use_container_width=True,
            type="primary")
            
with container:
    if submit_button:
        df = get_data(parameter, iso_start_time.isoformat(), iso_end_time.isoformat())
        st.session_state.df = df

        ## Calculations
        df = st.session_state.df
        mean_value = df["value"].mean()
        rolling_avg = df["value"].rolling(500, center=True).mean()

        # Plot parameter
        fig, ax = plt.subplots(figsize=[5,5])

        ## Plots
        df.set_index("timestamp").value.plot(ax=ax, lw=1)
        ax.axhline(y=mean_value, ls="dashed", lw=2, c="black")
        ax.plot(df["timestamp"], rolling_avg)

        ## Styling
        ax.set_ylabel(f"{parameter.title().replace('_', ' ')}")
        ax.spines[["top","right"]].set_visible(False)
        ax.legend([
                "Raw data", 
                f"Mean value = {mean_value:.1f}",
                "Rolling avg"],
            loc="center left",
            bbox_to_anchor=[1.02, 0.5],
            title=parameter.title().replace("_", " "))
        ax.set_xlabel("Date")
        st.pyplot(fig)
    else:
        st.info(" 👈 Select options from the sidebar")