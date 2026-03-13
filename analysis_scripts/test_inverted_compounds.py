import json


def simulate_with_inverted_offsets(race, soft_offset, hard_offset, soft_deg, hard_deg):
    """
    Test with HARD being faster (negative offset)
    """
    config = race['race_config']
    total_laps = config['total_laps']
    base_lap_time = config['base_lap_time']
    pit_lane_time = config['pit_lane_time']

    tire_offsets = {
        'SOFT': soft_offset,
        'MEDIUM': 0.0,
        'HARD': hard_offset
    }

    tire_degradation = {
        'SOFT': soft_deg,
        'MEDIUM': 0.05,
        'HARD': hard_deg
    }

    driver_times = {}

    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']
        driver_id = strategy['driver_id']

        total_time = 0
        current_tire = strategy['starting_tire']
        tire_age = 0
        pit_index = 0

        for lap in range(1, total_laps + 1):
            if pit_index < len(strategy['pit_stops']):
                pit_stop = strategy['pit_stops'][pit_index]
                if lap == pit_stop['lap']:
                    total_time += pit_lane_time
                    current_tire = pit_stop['to_tire']
                    tire_age = 0
                    pit_index += 1

            tire_age += 1

            tire_offset = tire_offsets[current_tire]
            deg_rate = tire_degradation[current_tire]
            degradation = deg_rate * tire_age
            lap_time = base_lap_time + tire_offset + degradation
            total_time += lap_time

        driver_times[driver_id] = total_time

    sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
    predicted = [d for d, t in sorted_drivers]
    actual = race['finishing_positions']

    matches = sum(1 for p, a in zip(predicted, actual) if p == a)
    return matches / 20 * 100


races = json.load(open('../data/historical_races/races_00000-00999.json'))

print("=" * 80)
print("TESTING INVERTED COMPOUND HYPOTHESIS")
print("HARD tires are FASTER and degrade SLOWER")
print("=" * 80)

# Test different combinations
test_cases = [
    # (name, soft_offset, hard_offset, soft_deg, hard_deg)
    ("SOFT=+0.1, HARD=-0.1, soft_deg=0.08, hard_deg=0.01", 0.1, -0.1, 0.08, 0.01),
    ("SOFT=+0.2, HARD=-0.2, soft_deg=0.08, hard_deg=0.01", 0.2, -0.2, 0.08, 0.01),
    ("SOFT=+0.15, HARD=-0.15, soft_deg=0.1, hard_deg=0.01", 0.15, -0.15, 0.1, 0.01),
    ("SOFT=+0.1, HARD=-0.1, soft_deg=0.1, hard_deg=0.02", 0.1, -0.1, 0.1, 0.02),
    ("SOFT=+0.05, HARD=-0.05, soft_deg=0.06, hard_deg=0.01", 0.05, -0.05, 0.06, 0.01),
]

best_accuracy = 0
best_config = None

for name, soft_off, hard_off, soft_deg, hard_deg in test_cases:
    total_accuracy = 0
    races_tested = min(100, len(races))

    for race in races[:races_tested]:
        accuracy = simulate_with_inverted_offsets(race, soft_off, hard_off, soft_deg, hard_deg)
        total_accuracy += accuracy

    avg_accuracy = total_accuracy / races_tested

    print(f"\n{name}")
    print(f"  Accuracy: {avg_accuracy:.1f}%")

    if avg_accuracy > best_accuracy:
        best_accuracy = avg_accuracy
        best_config = (name, soft_off, hard_off, soft_deg, hard_deg)

print("\n" + "=" * 80)
print(f"BEST CONFIG: {best_config[0]}")
print(f"ACCURACY: {best_accuracy:.1f}%")
print("=" * 80)