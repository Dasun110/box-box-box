import json
import statistics

races = json.load(open('../data/historical_races/races_00000-00999.json'))


def analyze_race_degradation(race):
    """Calculate actual degradation happening in this race"""
    config = race['race_config']
    track_temp = config['track_temp']
    base_lap_time = config['base_lap_time']
    total_laps = config['total_laps']
    pit_lane_time = config['pit_lane_time']

    # For drivers with only 1 pit stop, we can estimate degradation
    one_pit_drivers = []

    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']
        driver_id = strategy['driver_id']

        if len(strategy['pit_stops']) == 1:
            pit_stop = strategy['pit_stops'][0]
            pit_lap = pit_stop['lap']

            # Estimate:
            # Laps 1 to pit_lap: on starting tire (degrades)
            # Laps pit_lap+1 to total: on new tire (fresh)

            finishing_order = race['finishing_positions']
            finishing_pos = finishing_order.index(driver_id) + 1

            one_pit_drivers.append({
                'driver_id': driver_id,
                'finishing_pos': finishing_pos,
                'starting_tire': strategy['starting_tire'],
                'first_stint_laps': pit_lap - 1,  # Laps before pit
                'second_stint_laps': total_laps - pit_lap,
                'pit_lap': pit_lap
            })

    return {
        'race_id': race['race_id'],
        'track': config['track'],
        'temp': track_temp,
        'base_lap_time': base_lap_time,
        'total_laps': total_laps,
        'pit_lane_time': pit_lane_time,
        'one_pit_drivers': one_pit_drivers
    }


# Group races by temperature
temp_analysis = {}

for race in races:
    analysis = analyze_race_degradation(race)
    temp = analysis['temp']

    if temp not in temp_analysis:
        temp_analysis[temp] = {
            'races': [],
            'drivers': []
        }

    temp_analysis[temp]['races'].append(analysis)
    temp_analysis[temp]['drivers'].extend(analysis['one_pit_drivers'])

print("=" * 80)
print("DEGRADATION ANALYSIS BY TEMPERATURE")
print("=" * 80)

for temp in sorted(temp_analysis.keys()):
    drivers = temp_analysis[temp]['drivers']

    if not drivers:
        continue

    # Group by starting tire
    by_tire = {'SOFT': [], 'MEDIUM': [], 'HARD': []}

    for driver in drivers:
        by_tire[driver['starting_tire']].append(driver)

    print(f"\nTemperature: {temp}°C ({len(drivers)} drivers across {len(temp_analysis[temp]['races'])} races)")

    for tire in ['SOFT', 'MEDIUM', 'HARD']:
        tire_drivers = by_tire[tire]

        if tire_drivers:
            positions = [d['finishing_pos'] for d in tire_drivers]
            stints = [d['first_stint_laps'] for d in tire_drivers]

            avg_pos = statistics.mean(positions)
            avg_stint = statistics.mean(stints)

            print(f"  {tire:6s}: {len(tire_drivers):3d} drivers, "
                  f"avg pos={avg_pos:5.1f}, avg first stint={avg_stint:5.1f} laps")

print("\n" + "=" * 80)
print("OBSERVATION: Does temperature affect first stint length?")
print("=" * 80)

# For each track, analyze how temperature affects pit timing
from collections import defaultdict

track_temp_analysis = defaultdict(lambda: defaultdict(list))

for race in races:
    config = race['race_config']
    track = config['track']
    temp = config['track_temp']

    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']

        if len(strategy['pit_stops']) == 1:
            pit_lap = strategy['pit_stops'][0]['lap']
            track_temp_analysis[track][temp].append(pit_lap)

for track in sorted(track_temp_analysis.keys()):
    temps = sorted(track_temp_analysis[track].keys())

    if len(temps) > 2:
        print(f"\n{track}:")
        for temp in temps[:3] + temps[-3:]:  # First 3 and last 3 temps
            pit_laps = track_temp_analysis[track][temp]
            avg_pit_lap = statistics.mean(pit_laps)
            print(f"  {temp:2d}°C: avg pit lap = {avg_pit_lap:5.1f}")