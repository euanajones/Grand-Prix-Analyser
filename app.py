import streamlit as st
from src import api_handler

st.title("Formula One Grand Prix Analyser")

season = st.selectbox(
    "Please select a Formula One season:",
    ["2020", "2021", "2022", "2023", "2024"]
)

track = st.selectbox(
    "Please select a Formula One track:",
    ["Monaco", "Silverstone", "Monza", "Suzuka"]
)

search = st.button('Search for Drivers', type="secondary")

if search:
    driver_data_status = st.text('Loading driver data...')
    available_drivers = api_handler.getDrivers(int(season), track)
    driver_data_status.text('Driver data collected!')

    drivers = st.multiselect(
        "Please select your Formula One drivers:",
        available_drivers,
    )
