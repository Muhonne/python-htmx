import json
from datetime import datetime, timedelta
import random

# Initialize variables
start_time = datetime.utcnow()
num_entries = 24*60  # Number of minutes in one hour
data = []

# Generate mock data
for i in range(num_entries):
    timestamp = start_time + timedelta(minutes=i)
    entry = {
        "timestamp": timestamp.isoformat() + "Z",
        "heartRate": random.randint(60, 100),
        "hrv": random.randint(30, 70),
        "breathsPerMinute": random.randint(12, 20)
    }
    data.append(entry)

# Write to JSON file
with open('timeseries_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Mock data written to timeseries_data.json")