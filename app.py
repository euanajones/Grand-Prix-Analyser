import streamlit as st
from src import api_handler

st.title("Formula One Grand Prix Analyser")

# Initialise session state for drivers if not already set
if "available_drivers" not in st.session_state:
    st.session_state.available_drivers = []
    st.session_state.tracks = []

season = st.selectbox(
    "Please select a Formula One season:",
    ["2020", "2021", "2022", "2023", "2024"]
)
season = int(season)

season_select = st.button('Select Season', type="primary")

if season_select:
    track_data_status = st.text('Loading track data...')
    st.session_state.tracks = api_handler.getTracks(season)
    track_data_status.text('Track data collected!')

track = st.selectbox(
    "Please select a Formula One track:",
    st.session_state.tracks
)

search = st.button('Search for Drivers', type="primary")

if search:
    driver_data_status = st.text('Loading driver data...')
    st.session_state.session, st.session_state.available_drivers = api_handler.getDrivers(season, track)
    driver_data_status.text('Driver data collected!')

# Use session_state to populate the driver selectbox
driver = st.selectbox(
    "Please select your Formula One driver:",
    st.session_state.available_drivers,
)

select = st.button('Select Driver', type="primary")

if select:
    driver_id = driver.split(" - ")[0]  # Extract driver ID from the selected option
    lap_data_status = st.text('Loading lap data...')
    selected_driver, selected_driver_data = api_handler.getDriverLapData(st.session_state.session, driver_id)
    lap_data_status.text('Lap data collected!')

    api_handler.displayDriverData(st.session_state.session, selected_driver, selected_driver_data)
