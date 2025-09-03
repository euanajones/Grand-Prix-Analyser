# Grand Prix Analyser
A python script using the FastF1 API, that analyses selected driver performance at a specified GP. Produces a graphical output using matplotlib to visualise lap time data and its correlation between a change in tyre compounds when comparing it with the lap time mean average.

## About FastF1 API 
FastF1 gives access to F1 lap timing, car telemetry and position, tyre data, weather data, the event schedule and session results, utilising pandas to store data in dataframes.

More info about FastF1 API can be found here: [FastF1 API Documentation](https://docs.fastf1.dev/)

## How to run
Clone the repo from github in whatever way you choose.
Make sure your working director is grand-prix-analyser
```
cd grand-prix-analyser
```
Once you are in the correct directory, you should install all dependancies (ideally in a venv so as to not clutter up your machine)
```
pip install -r requirements.txt
```
Now you can run the app using:
```
streamlit run app.py
```

## Known Issues
I have found that there are some issues with using the FastF1 API to access data from older seasons, particularly pre-2020. When loading a session the API will present a warning message, where you will have to manually terminate the script and rerun it with a new season and or track.
I am looking to fix this issue by prompting the user with a more detailed error message and to select a different season and or track, removing the need to rerun the script again.
