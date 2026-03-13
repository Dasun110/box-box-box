import json


def analyze_race_performance(race):
    """
    For each driver, calculate their average lap time
    """
    config = race['race_config']
    total_laps = config['total_laps']

    # We need to find drivers' total times from finishing positions
    # But we don't have that directly - we only have finishing order

    # However, we can use this logic:
    # If we know the finishing order and calculate each driver's time,
    # the finishing order should match

    results = []

    for pos in range(1, 21):
        pos_key = f'pos{pos}'
        strategy = race['strategies'][pos_key]
        driver_id = strategy['driver_id']

        # Find this driver's finishing position
        finishing_order = race['finishing_positions']
        finishing_pos = finishing_order.index(driver_id) + 1

        results.append({
            'driver_id': driver_id,
            'finishing_position': finishing_pos,
            'starting_tire': strategy['starting_tire'],
            'pit_stops': len(strategy['pit_stops']),
            'strategy': strategy
        })

    return results


races = json.load(open('../data/historical_races/races_00000-00999.json'))
race = races[0]

print(f"Analyzing race: {race['race_id']}")
print(f"Track: {race['race_config']['track']}")
print(f"Total laps: {race['race_config']['total_laps']}")
print(f"Base lap time: {race['race_config']['base_lap_time']}")
print(f"Pit lane time: {race['race_config']['pit_lane_time']}")
print(f"Track temp: {race['race_config']['track_temp']}")

results = analyze_race_performance(race)
print("\n=== RESULTS ===")
for r in results:
    print(f"{r['finishing_position']:2d}. {r['driver_id']} "
          f"(starts: {r['starting_tire']:6s}, pits: {r['pit_stops']})")