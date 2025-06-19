import fastf1
import fastf1.plotting
import os
from matplotlib import pyplot as plt

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

year = int(input("Please select a year in Formula One: "))
track = input("Please select a track on the calendar for this year: ")

TYPE = 'R'

# Loads session data from FastF1 API call
try:
    session = fastf1.get_session(year, track, TYPE)
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

# Saves lap:compound data into a dictionary
for x in tyre_change:
    compound = selected_driver_data.pick_lap(x)['Compound']
    tyre_change[x] = compound.to_string(index=False)

# Normalise data to remove In/Out Laps, SVC Laps, etc
laptime_seconds = selected_driver_data['LapTime'].dt.total_seconds()
mean_laptime_seconds = laptime_seconds.mean()
laptime_std_dev = laptime_seconds.std()

# Normalised data stored as a dataframe, holds 95% of data about the mean
normal_driver_data = selected_driver_data.loc[(laptime_seconds < mean_laptime_seconds + (2 * laptime_std_dev)) & (laptime_seconds > mean_laptime_seconds - (2 * laptime_std_dev)), :]

x = normal_driver_data['LapNumber']
y = normal_driver_data['LapTime']

# Plotting styles
compounds = ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET', 'TEST_UNKNOWN', 'UNKNOWN']
compound_color_map = ['red', 'yellow', 'white', 'green', 'blue', 'gray', 'gray']

fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

fig, ax = plt.subplots()
ax.plot(x, y, label=selected_driver['FullName'])

init_compound = normal_driver_data.loc[normal_driver_data['LapNumber'] == 1, 'Compound'].to_string(index=False)
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
ax.set_title('Lap Time Per Lap')
ax.legend()
plt.show()