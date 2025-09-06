import pandas as pd
import fastf1

def collectData():
    all_race_data = []

    for year in range(2022, 2025):
        try:
            season_schedule = fastf1.get_event_schedule(year)
        except Exception as e:
            print(f"Error occurred when accessing FastF1 API schedule for {year}: {e}")
            exit(0)

        for index, event in season_schedule.iterrows():
            if event['EventFormat'] != 'conventional':
                continue
            
            try:
                session = fastf1.get_session(year, event['RoundNumber'], 'R')
                session.load(telemetry=False, weather=False) # Load only results data to minimise load time
                print(f"Processing: {event['EventName']}...")
            except Exception as e:
                print(f"Could not load session for {event['EventName']}: {e}")
                continue

            raceID = int(event['RoundNumber'])
            track = event['EventName']

            for _, driver_result in session.results.iterrows():
                try:  
                    # Remove erroneous data (GridPosition 0 or Points 26)
                    if driver_result['GridPosition'] == 0 or driver_result['Points'] == 26.0:
                        continue
                    row_data = {
                        "RaceID": raceID,
                        "Year": year,
                        "Track": track,
                        "Driver": driver_result['Abbreviation'],
                        "GridPosition": int(driver_result['GridPosition']),
                        "FinalPosition": int(driver_result['Position'])
                    }
                    all_race_data.append(row_data)
                except Exception as e:
                    print(f"Error occurred while processing results for {event['EventName']}: {e}")
                    continue

        df = pd.DataFrame(all_race_data)

        df['AvgGridPosition'] = round(df.groupby(['Year', 'Driver'])['GridPosition'].transform('mean'))
        df['AvgFinalPosition'] = round(df.groupby(['Year', 'Driver'])['FinalPosition'].transform('mean'))
        df['AvgHistoricalPosition'] = round(df.groupby(['Track', 'Driver'])['FinalPosition'].transform('mean'))
        df['AvgPositionChange'] = (df['AvgGridPosition'] - df['AvgFinalPosition'])

    df.fillna(0, inplace=True)

    model_data = getModelData(df)

    return model_data

def getModelData(df):
    model_data = [
        "Driver",
        "Track",
        "GridPosition",
        "AvgGridPosition",
        "AvgFinalPosition",
        "AvgHistoricalPosition",
        "AvgPositionChange",
        "FinalPosition"
    ]

    print("Model data collected!")
    # print(df[model_data].to_string(index=False))

    return df[model_data]