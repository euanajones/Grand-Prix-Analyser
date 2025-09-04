import fastf1
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def getTracks(year):
    try:
        schedule = fastf1.get_event_schedule(year)
    except Exception as e:
        print(f"Error occurred when accessing FastF1 API schedule for {year}: {e}")
        exit(0)

    tracks = schedule['EventName'].tolist()

    return tracks

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

    # Prepare normalised lap data
    x = normal_driver_data['LapNumber']
    y = normal_driver_data['LapTime'].dt.total_seconds()

    # Base scatter plot
    fig = px.scatter(
        x=x,
        y=y,
        labels={'x': 'Lap Number', 'y': 'Lap Time (s)'},
        title=f'Lap Time Per Lap at {session.event["EventName"]}'
    )

    # Add driver lap trace (line instead of scatter if preferred)
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name=driver['FullName'],
        line=dict(color='pink')
    ))

    # Shaded regions for above/below mean lap time
    fig.add_shape(type="rect",
                x0=min(x), x1=max(x),
                y0=mean_laptime_seconds, y1=max(y),
                fillcolor="red", opacity=0.2, line_width=0)

    fig.add_shape(type="rect",
                x0=min(x), x1=max(x),
                y0=min(y), y1=mean_laptime_seconds,
                fillcolor="green", opacity=0.2, line_width=0)

    # Tyre compound colours
    compounds = ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET', 'TEST_UNKNOWN', 'UNKNOWN']
    compound_color_map = ['red', 'yellow', 'white', 'green', 'blue', 'gray', 'gray']

    # Initial compound line
    init_compound = driver_data.loc[driver_data['LapNumber'] == 1, 'Compound'].to_string(index=False)
    init_comp_index = compounds.index(init_compound)
    init_comp_color = compound_color_map[init_comp_index]

    fig.add_vline(
        x=1,
        line=dict(color=init_comp_color, dash="dot"),
        annotation_text=init_compound,
        annotation_position="top"
    )

    # Tyre change vertical lines
    for lap, current_compound in tyre_change.items():
        comp_index = compounds.index(current_compound)
        comp_color = compound_color_map[comp_index]

        fig.add_vline(
            x=lap,
            line=dict(color=comp_color, dash="dot"),
            annotation_text=current_compound,
            annotation_position="top"
        )

    fig.update_layout(
        legend=dict(title="Drivers"),
        template="plotly_white",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    st.plotly_chart(fig)
