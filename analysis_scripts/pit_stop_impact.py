import json
from collections import defaultdict

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Group drivers by number of pit stops
pit_stop_results = defaultdict(list)

for race in races[:200]:  # Sample first 200 races
    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']
        driver_id = strategy['driver_id']
        num_pits = len(strategy['pit_stops'])

        finishing_order = race['finishing_positions']
        finishing_pos = finishing_order.index(driver_id) + 1

        pit_stop_results[num_pits].append(finishing_pos)

print("=" * 60)
print("PIT STOPS vs FINISHING POSITION")
print("=" * 60)

for num_pits in sorted(pit_stop_results.keys()):
    positions = pit_stop_results[num_pits]
    avg = sum(positions) / len(positions)
    print(f"\n{num_pits} pit stops:")
    print(f"  Drivers: {len(positions)}")
    print(f"  Avg position: {avg:.1f}")
    print(f"  Range: {min(positions)}-{max(positions)}")