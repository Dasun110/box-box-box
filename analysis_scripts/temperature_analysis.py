import json
from collections import defaultdict

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Group races by temperature
temp_groups = defaultdict(list)

for race in races:
    config = race['race_config']
    temp = config['track_temp']

    # Round to nearest 5°C for grouping
    temp_group = round(temp / 5) * 5

    temp_groups[temp_group].append({
        'race_id': race['race_id'],
        'track': config['track'],
        'base_lap_time': config['base_lap_time'],
        'actual_temp': temp,
        'total_laps': config['total_laps'],
        'finishing_positions': race['finishing_positions']
    })

print("=== TEMPERATURE GROUPS ===")
for temp in sorted(temp_groups.keys()):
    count = len(temp_groups[temp])
    tracks = set(r['track'] for r in temp_groups[temp])
    print(f"Temperature ~{temp}°C: {count} races, tracks: {tracks}")

# Now try to find if temperature affects lap times
# Compare same tracks at different temperatures
print("\n=== SAME TRACK, DIFFERENT TEMPS ===")

tracks_by_temps = defaultdict(lambda: defaultdict(list))
for race in races:
    config = race['race_config']
    track = config['track']
    temp = config['track_temp']
    tracks_by_temps[track][temp].append(race)

for track in sorted(tracks_by_temps.keys()):
    temps = sorted(tracks_by_temps[track].keys())
    if len(temps) > 1:
        print(f"\n{track}: temperatures {temps}")
        for temp in temps:
            count = len(tracks_by_temps[track][temp])
            print(f"  {temp}°C: {count} races")