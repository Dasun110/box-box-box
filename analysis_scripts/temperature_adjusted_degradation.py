import json


def simulate_with_temp_adjusted_deg(race, soft_offset, hard_offset, base_soft_deg, base_hard_deg):
    """
    Test: Does temperature affect degradation rate?
    """
    config = race['race_config']
    total_laps = config['total_laps']
    base_lap_time = config['base_lap_time']
    pit_lane_time = config['pit_lane_time']
    track_temp = config['track_temp']

    tire_offsets = {
        'SOFT': soft_offset,
        'MEDIUM': 0.0,
        'HARD': hard_offset
    }

    # Adjust degradation based on temperature
    # Higher temp = more degradation
    temp_factor = (track_temp - 27) * 0.001  # Normalize around 27°C

    tire_degradation = {
        'SOFT': base_soft_deg + temp_factor,
        'MEDIUM': 0.05 + temp_factor * 0.5,
        'HARD': base_hard_deg + temp_factor * 0.2
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
print("TESTING: Temperature-Adjusted Degradation")
print("=" * 80)

test_cases = [
    ("No temp adjust", 0.1, -0.1, 0.1, 0.01),
    ("Light temp adjust", 0.1, -0.1, 0.1, 0.01),
]

# For each case, test with temp adjustment
for name, soft_off, hard_off, base_soft_deg, base_hard_deg in test_cases:
    total_accuracy = 0
    races_tested = min(100, len(races))

    for race in races[:races_tested]:
        accuracy = simulate_with_temp_adjusted_deg(
            race, soft_off, hard_off, base_soft_deg, base_hard_deg
        )
        total_accuracy += accuracy

    avg_accuracy = total_accuracy / races_tested

    print(f"\n{name}:")
    print(f"  SOFT={soft_off:+.2f}, HARD={hard_off:+.2f}, "
          f"soft_deg={base_soft_deg:.2f}, hard_deg={base_hard_deg:.2f}")
    print(f"  Accuracy: {avg_accuracy:.1f}%")