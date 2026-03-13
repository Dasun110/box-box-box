import json

# Load first batch of historical races
races = json.load(open('data/historical_races/races_00000-00999.json'))

print("=" * 60)
print("PHASE 2: DATA EXPLORATION")
print("=" * 60)

print(f"\nTotal races loaded: {len(races)}")
print(f"\nSample race structure:")
print(f"Race ID: {races[0]['race_id']}")
print(f"Track: {races[0]['race_config']['track']}")
print(f"Total laps: {races[0]['race_config']['total_laps']}")
print(f"Base lap time: {races[0]['race_config']['base_lap_time']}")
print(f"Pit lane time: {races[0]['race_config']['pit_lane_time']}")
print(f"Track temperature: {races[0]['race_config']['track_temp']}°C")

print(f"\nFirst driver strategy:")
pos1 = races[0]['strategies']['pos1']
print(f"Driver: {pos1['driver_id']}")
print(f"Starting tire: {pos1['starting_tire']}")
print(f"Pit stops: {len(pos1['pit_stops'])}")
if pos1['pit_stops']:
    for pit in pos1['pit_stops']:
        print(f"  - Lap {pit['lap']}: {pit['from_tire']} → {pit['to_tire']}")

print(f"\nFinishing positions (fastest to slowest):")
for i, driver in enumerate(races[0]['finishing_positions'][:5], 1):
    print(f"{i}. {driver}")
print("...")

print("\n" + "=" * 60)
print("✅ Data loaded successfully!")
print("=" * 60)