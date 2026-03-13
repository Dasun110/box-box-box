import json
from collections import defaultdict

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Find races where:
# 1. All drivers use NO pit stops (same tire entire race)
# 2. Compare performance by tire compound

tire_performance = defaultdict(list)

for race in races:
    config = race['race_config']
    no_pit_races = []

    # Check if any drivers have no pit stops
    for pos in range(1, 21):
        pos_key = f'pos{pos}'
        strategy = race['strategies'][pos_key]
        driver_id = strategy['driver_id']
        starting_tire = strategy['starting_tire']

        # If no pit stops, record this driver
        if len(strategy['pit_stops']) == 0:
            finishing_order = race['finishing_positions']
            finishing_pos = finishing_order.index(driver_id) + 1

            tire_performance[starting_tire].append({
                'race_id': race['race_id'],
                'finishing_pos': finishing_pos,
                'track': config['track'],
                'base_lap_time': config['base_lap_time'],
                'track_temp': config['track_temp'],
                'total_laps': config['total_laps']
            })

print("=== TIRE PERFORMANCE ANALYSIS ===")
for tire in ['SOFT', 'MEDIUM', 'HARD']:
    if tire_performance[tire]:
        positions = [r['finishing_pos'] for r in tire_performance[tire]]
        avg_position = sum(positions) / len(positions)
        print(f"\n{tire}:")
        print(f"  Occurrences: {len(tire_performance[tire])}")
        print(f"  Avg finishing position: {avg_position:.1f}")
        print(f"  Best: {min(positions)}, Worst: {max(positions)}")