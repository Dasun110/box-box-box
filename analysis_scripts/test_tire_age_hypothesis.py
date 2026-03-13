import json
import statistics

races = json.load(open('../data/historical_races/races_00000-00999.json'))


# Hypothesis: Winners pit to keep tires young
# Losers let tires degrade too much

def analyze_tire_age_in_race(race):
    """
    For each driver, calculate their average tire age when crossing finish line
    """
    config = race['race_config']
    total_laps = config['total_laps']

    driver_tire_ages = {}

    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']
        driver_id = strategy['driver_id']

        # Simulate to find tire age at end
        current_tire = strategy['starting_tire']
        tire_age = 0
        pit_index = 0
        tire_ages = []

        for lap in range(1, total_laps + 1):
            # Check pit stop
            if pit_index < len(strategy['pit_stops']):
                pit_stop = strategy['pit_stops'][pit_index]
                if lap == pit_stop['lap']:
                    current_tire = pit_stop['to_tire']
                    tire_age = 0
                    pit_index += 1

            # Increment tire age
            tire_age += 1
            tire_ages.append(tire_age)

        # Calculate metrics
        avg_age = statistics.mean(tire_ages)
        max_age = max(tire_ages)
        final_age = tire_ages[-1]

        finishing_order = race['finishing_positions']
        finishing_pos = finishing_order.index(driver_id) + 1

        driver_tire_ages[driver_id] = {
            'finishing_pos': finishing_pos,
            'avg_tire_age': avg_age,
            'max_tire_age': max_age,
            'final_tire_age': final_age
        }

    return driver_tire_ages


print("=" * 70)
print("TIRE AGE ANALYSIS: Winners vs Losers")
print("=" * 70)

# Analyze first few races
for race_idx in range(5):
    race = races[race_idx]
    tire_ages = analyze_tire_age_in_race(race)

    print(f"\n{race['race_id']} - {race['race_config']['track']}")
    print(f"Laps: {race['race_config']['total_laps']}")

    print("\nTOP 5:")
    top_5 = sorted(tire_ages.items(),
                   key=lambda x: x[1]['finishing_pos'])[:5]
    for driver_id, data in top_5:
        print(f"  {data['finishing_pos']:2d}. {driver_id}: "
              f"avg age={data['avg_tire_age']:.1f}, "
              f"max age={data['max_tire_age']}, "
              f"final age={data['final_tire_age']}")

    print("\nBOTTOM 5:")
    bottom_5 = sorted(tire_ages.items(),
                      key=lambda x: x[1]['finishing_pos'],
                      reverse=True)[:5]
    for driver_id, data in bottom_5:
        print(f"  {data['finishing_pos']:2d}. {driver_id}: "
              f"avg age={data['avg_tire_age']:.1f}, "
              f"max age={data['max_tire_age']}, "
              f"final age={data['final_tire_age']}")

# Statistical analysis
print("\n" + "=" * 70)
print("STATISTICAL CORRELATION: Tire Age vs Finishing Position")
print("=" * 70)

correlations = {
    'avg_tire_age': [],
    'max_tire_age': [],
    'final_tire_age': []
}

for race in races[:200]:
    tire_ages = analyze_tire_age_in_race(race)

    for driver_id, data in tire_ages.items():
        correlations['avg_tire_age'].append(
            (data['avg_tire_age'], data['finishing_pos'])
        )
        correlations['max_tire_age'].append(
            (data['max_tire_age'], data['finishing_pos'])
        )
        correlations['final_tire_age'].append(
            (data['final_tire_age'], data['finishing_pos'])
        )

# Calculate correlation
for metric in correlations:
    values = correlations[metric]
    ages = [v[0] for v in values]
    positions = [v[1] for v in values]

    # Simple correlation: average age of top 5 vs bottom 5
    top_5_ages = [a for a, p in values if p <= 5]
    bottom_5_ages = [a for a, p in values if p >= 16]

    if top_5_ages and bottom_5_ages:
        top_avg = statistics.mean(top_5_ages)
        bottom_avg = statistics.mean(bottom_5_ages)

        print(f"\n{metric}:")
        print(f"  Top 5 average: {top_avg:.2f}")
        print(f"  Bottom 5 average: {bottom_avg:.2f}")
        print(f"  Difference: {bottom_avg - top_avg:.2f} "
              f"({'Bottom OLDER' if bottom_avg > top_avg else 'Top OLDER'})")