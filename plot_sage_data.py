import pandas as pd
import matplotlib.pyplot as plt
import sage_data_client
import streamlit as st
from datetime import datetime, date

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 30%;
            transition: all 0.8s;
            opacity: 0.7;
        }

        [data-testid=stSidebar] [data-testid=stImage]:hover {
            opacity: 1.0;
            transform: rotate(180deg);
        }
    </style>
    """, unsafe_allow_html=True
)

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

def to_isodate(d:date, t:datetime) -> str:
    """ 
    Takes a date and a time and returns it formatted in
    its ISO form for query submission
    """
    return datetime(
        d.year, d.month, d.day,
        t.hour, t.minute, t.second) 

"# 📈 Plot data from a SAGE node"
container = st.container()

with st.sidebar:
    st.image("https://portal.sagecontinuum.org/wsn-closed.dfca4c4b.png")
    with st.form("Form"):
        
        "## ⚙️ Parameter:"
        parameter = st.selectbox(
            "Select one", 
            ["temperature", "relative_humidity", "pressure"],
            format_func=lambda x:x.title().replace("_"," "))

        "## 🗓️ Time range:"
        
        date_range = st.date_input(
            "Dates range",
            [date(2023, 2, 8), date(2023, 2, 11)],
            label_visibility="collapsed")
        
        start_date, end_date = date_range
        
        cols = st.columns(2)
        with cols[0]: start_time = st.time_input("Start time")
        with cols[1]: end_time = st.time_input("End time")

        iso_start_time = to_isodate(start_date, start_time)
        iso_end_time = to_isodate(end_date, end_time)
        
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