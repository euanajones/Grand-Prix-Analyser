import fastf1
import os

# Handles cache directory to improve API performance
try:
    os.mkdir('cache')
    print*("Cache directory successfully created.")
except FileExistsError:
    print("Directory 'cache' already exists.")
except PermissionError:
    print("Permission Denied: Unable to create 'cache' directory due to too low permissions.")
except Exception as e:
    print(f"Creation of 'cache' directory has resulted in an error: {e}")

fastf1.Cache.enable_cache('cache')

YEAR = 2024
TRACK = 'Silverstone'
TYPE = 'R'

# Loads session data from FastF1 API call
try:
    session = fastf1.get_session(YEAR, TRACK, TYPE)
    session.load()
except Exception as e:
    print(f"Error occured when accessing FastF1 API sessions: {e}")
    exit(0)

print("--------------------------------------------")

print(f"{session.event['OfficialEventName']} \n")

print("The competing drivers for this session are:")
available_drivers = session.drivers

# Loops through array of driver numbers and assigns them to driver object
for driver_num in available_drivers:
    current_driver = session.get_driver(driver_num)
    print(f"{driver_num} - {current_driver['FullName']} ({current_driver['Abbreviation']})") # Uses driver object to pull data

print("--------------------------------------------")

selected_driver_id = input("Please select a driver using their number or abbreviated name: \n")

# Creates driver object from user selection
try:
    selected_driver = session.get_driver(selected_driver_id)
except Exception as e:
    print(f"An error occured whilst searching for driver {selected_driver_id}: {e}")
    exit(0)

print(f"\nYou have selected {selected_driver['BroadcastName']} ({selected_driver['CountryCode']}), part of the {selected_driver['TeamName']} F1 Team.")

print(f"Here is all lap data for {selected_driver['Abbreviation']}")

# Uses FastF1 API to pull specified driver lap data
selected_driver_num = selected_driver['DriverNumber']
selected_driver_data = session.laps.pick_drivers(selected_driver_num)

print(selected_driver_data.loc[:, ['Driver', 'LapNumber', 'LapTime', 'Stint', 'Compound', 'TyreLife']].to_string(index=False))

# Converts pandas stint series into list
stint_data = selected_driver_data['Stint'].to_list()

tyre_change = {}

for i in range(len(stint_data)-1):
    current_stint = stint_data[i]

    if stint_data[i+1] != current_stint:
        current_stint = stint_data[i+1]

        tyre_change[i+2] = 'UNKNOWN'

for x in tyre_change:
    compound = selected_driver_data.pick_lap(x)['Compound']
    tyre_change[x] = compound.to_string(index=False)

print(str(tyre_change))
