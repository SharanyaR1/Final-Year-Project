import random
import time
import requests
import json

# The URL of your Flask API
BASE_URL = "http://127.0.0.1:5000"

# Function to generate random garbage bin levels
def generate_garbage_level():
    """Simulate the garbage level for a dustbin."""
    return random.randint(0, 100)  # Fullness in percentage (0-100)

# Function to simulate IoT sensor data and send it to the backend
def simulate_sensor_data():
    # Fetch existing dustbins from the backend
    response = requests.get(f"{BASE_URL}/dustbins")
    if response.status_code != 200:
        print(f"Failed to fetch dustbins: {response.text}")
        return
    
    dustbins = response.json()
    
    # Generate sensor data (garbage level) for each dustbin
    sensor_data = []
    for dustbin in dustbins:
        dustbin_id = dustbin['id']
        garbage_level = generate_garbage_level()
        sensor_data.append({
            'id': dustbin_id,
            'garbage_level': garbage_level
        })

    # Send the sensor data to the backend (this could update the dustbin information or be used for optimization)
    update_url = f"{BASE_URL}/update_dustbin_levels"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(update_url, data=json.dumps(sensor_data), headers=headers)
    
    if response.status_code == 200:
        print("Successfully updated dustbin levels")
    else:
        print(f"Failed to update dustbin levels: {response.text}")

# Main loop to simulate sensor data every 10 seconds
def main():
    while True:
        simulate_sensor_data()
        time.sleep(10)  # Simulate every 10 seconds

if __name__ == "__main__":
    main()
