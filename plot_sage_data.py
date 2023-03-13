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

"# 👋 Hello"
cols = st.columns([1,1])
with cols[0]: st.info(" 👈 Select one of the options from the sidebar")
with cols[1]: st.image("https://portal.sagecontinuum.org/wsn-closed.dfca4c4b.png")

with st.expander("**Useful links**", expanded=True):
    """
    - [🔗](https://docs.waggle-edge.ai/docs/about/overview) Waggle: A distributed software-defined sensor network.
    - [🔗](https://portal.sagecontinuum.org/nodes) Sage Portal.
    """