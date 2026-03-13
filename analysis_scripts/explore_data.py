import json
import os

# Load one file of historical races
def load_races(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Load the first batch of races
races = load_races('../data/historical_races/races_00000-00999.json')

print(f"Total races loaded: {len(races)}")
print(f"\nFirst race ID: {races[0]['race_id']}")
print(f"Keys in first race: {races[0].keys()}")

# Print the first race in pretty format
print("\n=== FIRST RACE ===")
print(json.dumps(races[0], indent=2))