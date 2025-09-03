import fastf1
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