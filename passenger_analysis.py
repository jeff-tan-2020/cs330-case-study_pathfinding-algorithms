import pandas as pd

# Read CSV file into a pandas DataFrame
df = pd.read_csv('results/t5rides_final.csv', parse_dates=[0, 1])

# Calculate the time difference between passenger_start_datetime and ride_match_datetime
df['time_difference'] = (df['ride_match_datetime'] - df['passenger_start_datetime']).dt.total_seconds()

# Add the time difference to the other columns
df['total_passenger_time'] = (3600*df['driver_to_passenger'] + 3600*df['passenger_to_dest'] + 
                              df['time_difference'] + df['match_runtime_sec'])

# Drop the 'time_difference' column if you don't need it anymore
df = df.drop(columns=['time_difference'])

# Save the modified DataFrame back to a CSV file
df['total_passenger_time'].to_csv('results/t5_passenger_final.csv', index=False)