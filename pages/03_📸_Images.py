import streamlit as st
from datetime import date, time
from itertools import cycle
from appmisc import *

## Not implemented yet
st.session_state.form_submitted = False
def make_persistent(): st.session_state.form_submitted = True

with open("./assets/style.css") as f:
    st.markdown(f"""
        <style>{f.read()}</style>
        """, unsafe_allow_html=True)

parameters = {
    "bottom" : "Bottom camera",
    "top" : "Top camera", 
    "left" : "Left camera"}

"# 📸 Images from the SAGE node"
container = st.container()

if check_password():
    with st.sidebar:
        st.image("https://portal.sagecontinuum.org/wsn-closed.dfca4c4b.png")
        with st.form("Form"):
            
            "## ⚙️ Parameter:"
            parameter = st.selectbox(
                "Parameter", 
                parameters.keys(),
                format_func=lambda x:parameters[x],
                label_visibility="collapsed")
            
            "## 📍 Node:"
            node_id = st.selectbox("Node", ["W083", "W024", "W014"], label_visibility="collapsed")

            "## 🗓️ Time range:"
            
            date_range = st.date_input(
                "Dates range",
                date(2023, 3, 4),
                label_visibility="collapsed")
            
            start_date = date_range
            end_date = date_range
            
            cols = st.columns(2)
            with cols[0]: start_time = st.time_input("Start time", time(4,0,0))
            with cols[1]: end_time = st.time_input("End time", time(9,0,0))

            iso_start_time = to_isodate(start_date, start_time)
            iso_end_time = to_isodate(end_date, end_time)
            
            # Retrieve data
            submit_button = st.form_submit_button(
                "Retrive data and plot", 
                use_container_width=True,
                type="primary",
                on_click=make_persistent)

    with container:
        if submit_button:
            imgs, df = get_images(
                parameter,
                node_id,
                iso_start_time.isoformat(),
                iso_end_time.isoformat()
            )

            if len(imgs) == 0:
                st.warning("No images were found", icon="🌌")
            
            else:
                cols = st.columns(3)
                cycle_cols = cycle(cols)

                for t,f,col in zip(df.timestamp, imgs, cycle_cols):
                    with col:
                        st.caption(f"*{t.strftime('%A, %d %B %Y %I:%M%p')}*")
                        st.image(f, use_column_width=True)

            # for f in os.listdir('images'):
            #     st.image(f'images/{f}')

