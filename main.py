import fastf1
import os

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

try:
    session = fastf1.get_session(YEAR, TRACK, TYPE)
    session.load()
except Exception as e:
    print(f"Error occured when accessing FastF1 API sessions: {e}")
    exit(0)

print("--------------------------------------------")

print(f"{session.event['OfficialEventName']}")
print(f"{session.event['EventDate']} \n")
print("The competing drivers for this session are:")

available_drivers = session.drivers

for driverNum in available_drivers:
    current_driver = session.get_driver(driverNum)
    print(f"{driverNum} - {current_driver['FullName']} ({current_driver['Abbreviation']})")

print("--------------------------------------------")
