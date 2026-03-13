import json
import statistics

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# For drivers with exactly 1 pit stop
# Estimate tire performance degradation per compound

compound_degradation = {
    'SOFT': {'first_stints': [], 'finishing_positions': []},
    'MEDIUM': {'first_stints': [], 'finishing_positions': []},
    'HARD': {'first_stints': [], 'finishing_positions': []}
}

for race in races[:500]:
    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']
        driver_id = strategy['driver_id']

        if len(strategy['pit_stops']) == 1:
            starting_tire = strategy['starting_tire']
            pit_lap = strategy['pit_stops'][0]['lap']
            first_stint_laps = pit_lap - 1

            finishing_order = race['finishing_positions']
            finishing_pos = finishing_order.index(driver_id) + 1

            compound_degradation[starting_tire]['first_stints'].append(first_stint_laps)
            compound_degradation[starting_tire]['finishing_positions'].append(finishing_pos)

print("=" * 80)
print("COMPOUND-SPECIFIC DEGRADATION ANALYSIS")
print("=" * 80)

for compound in ['SOFT', 'MEDIUM', 'HARD']:
    data = compound_degradation[compound]

    if data['first_stints']:
        stints = data['first_stints']
        positions = data['finishing_positions']

        # Group by stint length ranges
        short_stint = [p for s, p in zip(stints, positions) if s < 10]
        medium_stint = [p for s, p in zip(stints, positions) if 10 <= s < 20]
        long_stint = [p for s, p in zip(stints, positions) if s >= 20]

        print(f"\n{compound}:")
        print(f"  Total drivers: {len(stints)}")
        print(f"  Stint length - avg: {statistics.mean(stints):.1f}, "
              f"range: {min(stints)}-{max(stints)}")

        if short_stint:
            print(f"  Short stint (<10 laps): {len(short_stint)} drivers, "
                  f"avg finish: {statistics.mean(short_stint):.1f}")
        if medium_stint:
            print(f"  Medium stint (10-20 laps): {len(medium_stint)} drivers, "
                  f"avg finish: {statistics.mean(medium_stint):.1f}")
        if long_stint:
            print(f"  Long stint (20+ laps): {len(long_stint)} drivers, "
                  f"avg finish: {statistics.mean(long_stint):.1f}")

        # Correlation: longer stint = worse finishing?
        correlation = statistics.correlation(stints, positions) if len(stints) > 2 else 0
        print(f"  Correlation (stint length vs position): {correlation:.3f}")