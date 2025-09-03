import fastf1
from requests import session
import streamlit as st
from matplotlib import pyplot as plt

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

    return session, session_drivers

def getDriverLapData(session, driver_id):
    try:
        selected_driver = session.get_driver(driver_id)
    except Exception as e:
        print(f"An error occured whilst searching for driver {driver_id}: {e}")
        exit(0)

    st.write(f"\nYou have selected {selected_driver['BroadcastName']} ({selected_driver['CountryCode']}), part of the {selected_driver['TeamName']} F1 Team.")

    selected_driver_data = session.laps.pick_driver(driver_id)

    return selected_driver, selected_driver_data

def displayDriverData(session, driver, driver_data):
    # Converts pandas stint series into list
    stint_data = driver_data['Stint'].to_list()

    tyre_change = {}

    for i in range(len(stint_data)-1):
        current_stint = stint_data[i]

        if stint_data[i+1] != current_stint:
            current_stint = stint_data[i+1]

            tyre_change[i+2] = 'UNKNOWN'

    # Saves lap:compound data into a dictionary
    for x in tyre_change:
        compound = driver_data.pick_lap(x)['Compound']
        tyre_change[x] = compound.to_string(index=False)

    # Normalise data to remove In/Out Laps, SVC Laps, etc
    laptime_seconds = driver_data['LapTime'].dt.total_seconds()
    mean_laptime_seconds = laptime_seconds.mean()

    # Normalised data stored as a dataframe, removes 20% of most extreme data (lower 10% and upper 10% extremes)
    normal_driver_data = driver_data.loc[(laptime_seconds < mean_laptime_seconds * 1.1) & (laptime_seconds > mean_laptime_seconds * 0.9), :]

    x = normal_driver_data['LapNumber']
    y = normal_driver_data['LapTime'].dt.total_seconds()

    # Plotting styles
    compounds = ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET', 'TEST_UNKNOWN', 'UNKNOWN']
    compound_color_map = ['red', 'yellow', 'white', 'green', 'blue', 'gray', 'gray']

    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

    fig, ax = plt.subplots()
    ax.plot(x, y, label=driver['FullName'])

    y_min, y_max = ax.get_ylim()

    ax.axhspan(ymin=mean_laptime_seconds, ymax=y_max, color='red', alpha=0.3)
    ax.axhspan(ymin=y_min, ymax=mean_laptime_seconds, color='green', alpha=0.3)


    init_compound = driver_data.loc[driver_data['LapNumber'] == 1, 'Compound'].to_string(index=False)
    init_comp_index = compounds.index(init_compound)
    init_comp_color = compound_color_map[init_comp_index]

    ax.axvline(x=1, color=init_comp_color, label=init_compound, ls=':')

    for x in tyre_change.keys():
        current_compound = tyre_change.get(x)
        comp_index = compounds.index(current_compound)
        comp_color = compound_color_map[comp_index]

        ax.axvline(x=x, color=comp_color, label=current_compound, ls=':')

    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')
    ax.set_title(f'Lap Time Per Lap at \n {session.event['EventName']}')
    ax.legend()

    st.pyplot(fig)