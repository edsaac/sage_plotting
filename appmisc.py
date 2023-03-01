import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sage_data_client
import streamlit as st
from datetime import datetime, date, time

@st.cache_data
def get_data(
    parameter:str,
    node_id:str,
    start_datetime:str, end_datetime:str):

    """
    Queries the SAGE API for an environmental parameter
    """
    df = sage_data_client.query(
        start=start_datetime,
        end=end_datetime,
        filter={
            "name": f"env.{parameter}",
            "sensor": "bme680",
            "vsn":f"{node_id}",
        }
    )
    
    return df

@st.cache_data
def create_plotly_figure(df:pd.DataFrame, **kwargs) -> go.Figure:
    node_id = kwargs.get("node_id", "##")
    parameter = kwargs.get("parameter", "Parameter")

    mean_value = df["value"].mean()
    rolling_avg = df["value"].rolling(120, center=True).mean()

    fig = go.Figure()
    hovertemplate = """x = %{y:.1f} g <br> t = %{x}"""

    # Raw data
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=df["value"],
            name="Raw data",
            line=dict(color="rgba(1,135,73,0.5)", width=1),
            hovertemplate=hovertemplate
        )
    )

    # Rolling average
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=rolling_avg,
            name=f"Rolling average (1h)",
            line=dict(color="rgb(1,135,73)", width=2),
            hovertemplate=hovertemplate
        )
    )
    
    fig.update_layout(
        title_text=f"Node {node_id}",
        legend=dict(
            orientation="h",
            yanchor="bottom", y=0.99,
            xanchor="center", x=0.50
        ))

    fig.update_xaxes(
        title_text="Datetime", 
        showgrid=True)
    
    fig.update_yaxes(
        title_text=parameter.title().replace("_", " "), 
        showgrid=False)
    return fig

@st.cache_data
def create_matplotlib_figure(df:pd.DataFrame, **kwargs) -> plt.figure:
    node_id = kwargs.get("node_id", "##")
    parameter = kwargs.get("parameter", "Parameter")
    
    mean_value = df["value"].mean()
    rolling_avg = df["value"].rolling(120, center=True).mean()

    ## Plots
    fig, ax = plt.subplots(figsize=[5,5])
    
    df.set_index("timestamp").value.plot(
        ax=ax, lw=1, c="red",
        label="Raw data")
    ax.axhline(mean_value, lw=0.5, ls="dashed", c="green", label=f"Mean value = {mean_value:.1f}")
    ax.plot(df["timestamp"], rolling_avg, lw=2, c="blue", label="Rolling average")
    
    ## Styling
    ax.set_ylabel(f"{parameter.title().replace('_', ' ')}")
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="center left",
        bbox_to_anchor=[1.02, 0.5],
        title=parameter.title().replace("_", " "))
    ax.set_xlabel("Date")
    ax.set_title(f"Node {node_id}")

    return fig

def to_isodate(d:date, t:datetime) -> str:
    """ 
    Takes a date and a time and returns it formatted in
    its ISO form for query submission
    """
    return datetime(
        d.year, d.month, d.day,
        t.hour, t.minute, t.second) 