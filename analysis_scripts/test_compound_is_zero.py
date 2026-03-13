import json


def simulate_with_tire_offset(race, soft_offset, hard_offset):
    """Simulate with specific tire offsets"""
    config = race['race_config']
    total_laps = config['total_laps']
    base_lap_time = config['base_lap_time']
    pit_lane_time = config['pit_lane_time']

    tire_offsets = {
        'SOFT': soft_offset,
        'MEDIUM': 0.0,
        'HARD': hard_offset
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
            degradation = 0.01 * tire_age
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
print("TESTING: Are Tire Compounds ACTUALLY Different?")
print("=" * 80)

# Test: What if all compounds are EXACTLY the same (offset = 0)?
test_cases = [
    ("All same (0, 0)", 0.0, 0.0),
    ("SOFT -0.1, HARD +0.1", -0.1, 0.1),
    ("SOFT -0.2, HARD +0.2", -0.2, 0.2),
    ("SOFT +0.1, HARD -0.1", 0.1, -0.1),
]

print("\nWith degradation = 0.01 * tire_age:")
for name, soft_off, hard_off in test_cases:
    total_accuracy = 0
    races_tested = min(100, len(races))

    for race in races[:races_tested]:
        accuracy = simulate_with_tire_offset(race, soft_off, hard_off)
        total_accuracy += accuracy

    avg_accuracy = total_accuracy / races_tested
    print(f"  {name:30s} → {avg_accuracy:5.1f}%")