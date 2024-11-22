import random
import json

def generate_synthetic_data(num_bins=10):
    dustbins = []
    for _ in range(num_bins):
        latitude = random.uniform(12.9, 13.0)
        longitude = random.uniform(77.5, 77.6)
        capacity = random.randint(0, 100)
        dustbins.append({"latitude": latitude, "longitude": longitude, "capacity": capacity})
    with open("synthetic_dustbins.json", "w") as f:
        json.dump(dustbins, f)
    return dustbins
