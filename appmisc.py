import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sage_data_client
import streamlit as st
from datetime import datetime, date, time

@st.cache_data
def get_data(
    parameter:str,
    node_id:str,
    start_datetime:str, end_datetime:str,
    **kwargs):

    """
    Queries the SAGE API for an environmental parameter
    """
    is_rain = kwargs.get("is_rain", False)
    sensor = kwargs.get("sensor", "bme680") # Defaults to the environmental one

    if is_rain: 
        parameter = f"raingauge.{parameter}"
        sensor = "*"

    df = sage_data_client.query(
        start=start_datetime,
        end=end_datetime,
        filter={
            "name": f"env.{parameter}",
            "sensor": sensor,
            "vsn": node_id,
        }
    )

    print(f"env.{parameter}")
    return df

@st.cache_data
def create_environmental_figure(df:pd.DataFrame, **kwargs) -> go.Figure:
    node_id = kwargs.get("node_id", "##")
    parameter = kwargs.get("parameter", "Parameter")
    units = kwargs.get("units","")

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
        height=600,
        title_text=f"Node {node_id}",
        legend=dict(
            font_size=18,
            orientation="h",
            yanchor="bottom", y=0.99,
            xanchor="center", x=0.50
        ))

    fig.update_xaxes(
        title = dict(
            text="Date",
            font_size=20),
        showgrid=True)
    
    fig.update_yaxes(
        title = dict(
            text=parameter.title().replace("_", " ") + f" [{units}]",
            font_size=20), 
        showgrid=False)
    
    return fig

@st.cache_data
def create_rain_figure(df:pd.DataFrame, **kwargs) -> go.Figure:
    node_id = kwargs.get("node_id", "##")
    parameter = kwargs.get("parameter", "Parameter")
    units = kwargs.get("units","")

    mean_value = df["value"].mean()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    hovertemplate = """x = %{y:.1f} g <br> t = %{x}"""

    if "rain intensity" in parameter.lower():
        rolling_sum = df["value"].rolling(120, center=True).sum()

        # Raw data
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"], y=df["value"],
                mode="none",
                name="Raw data",
                fill="tozeroy",
                marker=dict(color="#4193BF", line_width=0),
                hovertemplate=hovertemplate
            ),
            secondary_y=False
        )

        # Rolling sum
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"], y=rolling_sum,
                name=f"Rolling sum (1h)",
                line=dict(color="#5B41BF", width=2),
                hovertemplate=hovertemplate
            ),
            secondary_y=True
        )

        fig.update_yaxes(
            title_text="Rolling sum (1h)", 
            showgrid=False, secondary_y=True, rangemode='tozero')


    else:
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"], y=df["value"],
                mode="none",
                name="Raw data",
                fill="tozeroy",
                marker=dict(color="rgba(31,120,180,0.9)", line_width=3),
                hovertemplate=hovertemplate
            ),
            secondary_y=False
        )

    fig.update_layout(
        height=600,
        title_text=f"Node {node_id}",
        legend=dict(
            font_size=18,
            orientation="h",
            yanchor="bottom", y=0.99,
            xanchor="center", x=0.50
        ))

    fig.update_xaxes(
        title = dict(
            text="Date",
            font_size=20),
        showgrid=True)
    
    fig.update_yaxes(
        title = dict(
            text=parameter.title().replace("_", " ") + f" [{units}]",
            font_size=20), 
        showgrid=False, secondary_y=False, rangemode='tozero')

    return fig

@st.cache_data
def create_matplotlib_figure(df:pd.DataFrame, **kwargs) -> plt.figure:
    node_id = kwargs.get("node_id", "##")
    parameter = kwargs.get("parameter", "Parameter")
    units = kwargs.get("units","")

    mean_value = df["value"].mean()
    rolling_avg = df["value"].rolling(120, center=True).mean()

    ## Plots
    fig, ax = plt.subplots(figsize=[5,5])
    
    df.set_index("timestamp").value.plot(
        ax=ax, lw=1, c="#1b9e77", alpha=0.6,
        label="Raw data")
    ax.axhline(mean_value, lw=0.5, ls="dashed", c="#d95f02", label=f"Mean value = {mean_value:.1f}")
    ax.plot(df["timestamp"], rolling_avg, lw=2, c="#1b9e77", label="Rolling average")
    
    ## Styling
    ax.set_ylabel(f"{parameter.title().replace('_', ' ')}")
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="center left",
        bbox_to_anchor=[1.02, 0.5],
        title=parameter.title().replace("_", " ") + f" [{units}]")
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

if __name__ == "main":
    pass