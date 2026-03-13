import json


def simulate_with_test_offsets(race, tire_offsets, degradation_model):
    """
    Test different tire offset combinations
    Return how many drivers we predict correctly
    """
    config = race['race_config']
    total_laps = config['total_laps']
    base_lap_time = config['base_lap_time']
    pit_lane_time = config['pit_lane_time']
    track_temp = config['track_temp']

    driver_times = {}

    for pos in range(1, 21):
        pos_key = f'pos{pos}'
        strategy = race['strategies'][pos_key]
        driver_id = strategy['driver_id']

        total_time = 0
        current_tire = strategy['starting_tire']
        tire_age = 0
        pit_index = 0

        for lap in range(1, total_laps + 1):
            # Handle pit stops
            if pit_index < len(strategy['pit_stops']):
                pit_stop = strategy['pit_stops'][pit_index]
                if lap == pit_stop['lap']:
                    total_time += pit_lane_time
                    current_tire = pit_stop['to_tire']
                    tire_age = 0
                    pit_index += 1

            # Increment tire age
            tire_age += 1

            # Calculate lap time
            tire_offset = tire_offsets.get(current_tire, 0)

            # Apply degradation model
            if degradation_model == 'linear':
                degradation = 0.05 * tire_age
            elif degradation_model == 'linear_soft_fast':
                # Different rates per compound
                rates = {'SOFT': 0.08, 'MEDIUM': 0.05, 'HARD': 0.02}
                degradation = rates[current_tire] * tire_age
            elif degradation_model == 'stepped':
                # No degradation first 5 laps, then increases
                if tire_age <= 5:
                    degradation = 0
                else:
                    degradation = 0.1 * (tire_age - 5)
            else:
                degradation = 0

            lap_time = base_lap_time + tire_offset + degradation
            total_time += lap_time

        driver_times[driver_id] = total_time

    # Check accuracy
    sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
    predicted = [d for d, t in sorted_drivers]
    actual = race['finishing_positions']

    matches = sum(1 for p, a in zip(predicted, actual) if p == a)

    return matches, predicted, actual


# Test many combinations
races = json.load(open('../data/historical_races/races_00000-00999.json'))

test_cases = [
    # (name, tire_offsets, degradation_model)
    ("SOFT=-1, MED=0, HARD=1, linear",
     {'SOFT': -1.0, 'MEDIUM': 0.0, 'HARD': 1.0}, 'linear'),

    ("SOFT=-1.5, MED=0, HARD=1.5, linear",
     {'SOFT': -1.5, 'MEDIUM': 0.0, 'HARD': 1.5}, 'linear'),

    ("SOFT=-0.5, MED=0, HARD=0.5, linear",
     {'SOFT': -0.5, 'MEDIUM': 0.0, 'HARD': 0.5}, 'linear'),

    ("SOFT=-1, MED=0, HARD=1, stepped",
     {'SOFT': -1.0, 'MEDIUM': 0.0, 'HARD': 1.0}, 'stepped'),

    ("SOFT=-1.5, MED=0, HARD=1.5, soft_fast_deg",
     {'SOFT': -1.5, 'MEDIUM': 0.0, 'HARD': 1.5}, 'linear_soft_fast'),
]

print("=" * 80)
print("TESTING DIFFERENT FORMULAS")
print("=" * 80)

best_matches = 0
best_config = None

for name, offsets, deg_model in test_cases:
    total_matches = 0
    races_tested = min(50, len(races))  # Test on first 50 races

    for race in races[:races_tested]:
        matches, _, _ = simulate_with_test_offsets(race, offsets, deg_model)
        total_matches += matches

    avg_matches = total_matches / races_tested / 20 * 100  # Convert to percentage

    print(f"\n{name}")
    print(f"  Accuracy: {avg_matches:.1f}%")

    if avg_matches > best_matches:
        best_matches = avg_matches
        best_config = (name, offsets, deg_model)

print("\n" + "=" * 80)
print(f"BEST SO FAR: {best_config[0]}")
print(f"Accuracy: {best_matches:.1f}%")
print("=" * 80)