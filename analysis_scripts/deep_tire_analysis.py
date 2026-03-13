import json
from collections import defaultdict
import statistics

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Track which tires perform better
tire_finishing = defaultdict(list)

for race in races:
    finishing_positions = race['finishing_positions']

    for pos, driver_id in enumerate(finishing_positions, 1):
        # Find this driver's strategy
        for pos_key in range(1, 21):
            strategy = race['strategies'][f'pos{pos_key}']
            if strategy['driver_id'] == driver_id:
                starting_tire = strategy['starting_tire']
                tire_finishing[starting_tire].append(pos)
                break

print("=" * 60)
print("TIRE PERFORMANCE: FINISHING POSITIONS")
print("=" * 60)

for tire in ['SOFT', 'MEDIUM', 'HARD']:
    positions = tire_finishing[tire]
    if positions:
        avg = statistics.mean(positions)
        median = statistics.median(positions)
        print(f"\n{tire}:")
        print(f"  Occurrences: {len(positions)}")
        print(f"  Average position: {avg:.1f}")
        print(f"  Median position: {median:.1f}")
        print(f"  Best: {min(positions)}, Worst: {max(positions)}")
        print(f"  Std Dev: {statistics.stdev(positions):.2f}")