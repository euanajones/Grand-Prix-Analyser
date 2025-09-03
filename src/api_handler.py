import fastf1
from requests import session
import streamlit as st

def getDrivers(year, track):
    try:
        session = fastf1.get_session(year, track, 'R')
        session.load()
    except Exception as e:
        print(f"Error occured when accessing FastF1 API sessions: {e}")
        exit(0)

    st.write(f"You have selected:\n{session.event['OfficialEventName']}")

    available_drivers = session.drivers
    session_drivers = []

    # Loops through array of driver numbers and assigns them to driver object
    for driver_num in available_drivers:
        current_driver = session.get_driver(driver_num)
        session_drivers.append(f"{driver_num} - {current_driver['FullName']} ({current_driver['Abbreviation']})") # Uses driver object to pull data

    return session_drivers

def getDriverLapData(year, track, driver_id):
    try:
        session = fastf1.get_session(year, track, 'R')
        session.load()
        selected_driver = session.get_driver(driver_id)
    except Exception as e:
        print(f"An error occured whilst searching for driver {driver_id}: {e}")
        exit(0)

    st.write(f"\nYou have selected {selected_driver['BroadcastName']} ({selected_driver['CountryCode']}), part of the {selected_driver['TeamName']} F1 Team.")

    selected_driver_data = session.laps.pick_driver(driver_id)

    return selected_driver_data