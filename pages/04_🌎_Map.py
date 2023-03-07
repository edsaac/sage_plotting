import streamlit as st
from appmisc import *
import folium
from streamlit_folium import st_folium
from statistics import mean

with open("./assets/style.css") as f:
    st.markdown(f"""
        <style>{f.read()}</style>
        """, unsafe_allow_html=True)

"# 🌎 Map of SAGE nodes"

st.info("Change the base map style on the sidebar", icon="👈")

nodes = ["W024", "W083"]

with st.sidebar:
    tiles = st.selectbox(
        "🌌 Pick a map style:", 
        [
            "OpenStreetMap", 
            "Stamen Terrain", 
            "Stamen Toner", 
            "Stamen Watercolor", 
            "CartoDB Positron", 
            "CartoDB Dark_Matter"
        ], 
        index=2)

coords = [ get_coordinates(node) for node in nodes ]
mid_coord = Coord(mean([c.lat for c in coords]), mean([c.lon for c in coords]))

## Draw the follium map
m = folium.Map(location=mid_coord, zoom_start=5, tiles=tiles)
for node,coord in zip(nodes, coords):
    folium.Marker(
        location=coord, 
        popup=f"<b>{node}</b>", 
        tooltip=f"<i>{node}</i>",
        icon=folium.Icon(icon="cloud")).add_to(m)

st_folium(m, width=700, height = 400, returned_objects=[])