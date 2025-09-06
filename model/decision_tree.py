from sklearn import tree
from model import data # Assuming this is your module to get the DataFrame
from sqlalchemy import create_engine, text
import numpy as np # Corrected alias from 'np' to 'numpy'

model_data = data.collectData()
engine = create_engine('sqlite://', echo=False)
model_data.to_sql('Model_Data', con=engine, if_exists='replace', index=False)

selected_driver = input("Enter the three-letter driver code (e.g., NOR, VER, HAM): ").upper()
# selected_track = input("Enter the track name (e.g., Monaco, Silverstone): ").title()
try:
    user_grid_position = int(input(f"Enter the starting grid position for {selected_driver}: "))
except ValueError:
    print("Invalid input. Grid position must be a whole number.")
else:
    with engine.connect() as conn:
        query_X = text(f"""
            SELECT GridPosition, AvgGridPosition, AvgFinalPosition, AvgHistoricalPosition, AvgPositionChange
            FROM Model_Data
            WHERE Driver = '{selected_driver}'
        """)
        query_Y = text(f"""
            SELECT FinalPosition
            FROM Model_Data
            WHERE Driver = '{selected_driver}'
        """)
        
        sample_data = conn.execute(query_X).fetchall()
        label_data = conn.execute(query_Y).fetchall()

    if not sample_data:
        print(f"Could not find any historical data for driver: {selected_driver}")
    else:
        X = sample_data
        Y = np.ravel(label_data)
        
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, Y)

        query_stats = text(f"""
            SELECT AvgGridPosition, AvgFinalPosition, AvgHistoricalPosition, AvgPositionChange
            FROM Model_Data
            WHERE Driver = '{selected_driver}'
            LIMIT 1
        """)
        with engine.connect() as conn:
            driver_stats = conn.execute(query_stats).fetchone()

        features = [user_grid_position] + list(driver_stats)
        prediction_input = np.array(features).reshape(1, -1)

        prediction = clf.predict(prediction_input)
        predicted_pos = prediction[0]

        print("-" * 40)
        print(f"Driver: {selected_driver}")
        # print(f"Track: {selected_track}")
        print(f"Starting Position: {user_grid_position}")
        print(f"Predicted Final Position: {predicted_pos:.0f}")
        print("-" * 40)
