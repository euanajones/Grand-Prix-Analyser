import fastf1

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
print(f"{session.event['EventDate']}")
print("Session Results:")
print(f"{session.results.loc[:, ['Position', 'DriverNumber', 'Abbreviation', 'BroadcastName', 'TeamName']].to_string(index=False)}")

print("--------------------------------------------")
