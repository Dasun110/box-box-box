import json


def simulate_with_inverted_offsets(race, soft_offset, hard_offset, soft_deg, hard_deg):
    """Test with inverted assumptions"""
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
print("GRID SEARCH: INVERTED COMPOUND MODEL")
print("=" * 80)

best_accuracy = 0
best_config = None

# Grid search
soft_offsets = [0.05, 0.1, 0.15, 0.2, 0.25]
hard_offsets = [-0.05, -0.1, -0.15, -0.2, -0.25]
soft_degs = [0.06, 0.08, 0.1, 0.12]
hard_degs = [0.01, 0.02, 0.03]

print(f"\nTesting {len(soft_offsets) * len(hard_offsets) * len(soft_degs) * len(hard_degs)} combinations...")
print("This may take a while...\n")

count = 0
for soft_off in soft_offsets:
    for hard_off in hard_offsets:
        for soft_deg in soft_degs:
            for hard_deg in hard_degs:
                total_accuracy = 0
                races_tested = min(50, len(races))

                for race in races[:races_tested]:
                    accuracy = simulate_with_inverted_offsets(
                        race, soft_off, hard_off, soft_deg, hard_deg
                    )
                    total_accuracy += accuracy

                avg_accuracy = total_accuracy / races_tested

                if avg_accuracy > best_accuracy:
                    best_accuracy = avg_accuracy
                    best_config = (soft_off, hard_off, soft_deg, hard_deg)
                    print(f"✅ New best: {best_accuracy:.1f}% "
                          f"(SOFT={soft_off:+.2f}, HARD={hard_off:+.2f}, "
                          f"soft_deg={soft_deg:.2f}, hard_deg={hard_deg:.2f})")

                count += 1
                if count % 20 == 0:
                    print(f"   Tested {count} combinations...")

print("\n" + "=" * 80)
if best_config:
    soft_off, hard_off, soft_deg, hard_deg = best_config
    print(f"BEST CONFIG FOUND:")
    print(f"  SOFT offset: {soft_off:+.2f} seconds")
    print(f"  HARD offset: {hard_off:+.2f} seconds")
    print(f"  SOFT degradation: {soft_deg:.2f} seconds/lap")
    print(f"  HARD degradation: {hard_deg:.2f} seconds/lap")
    print(f"  ACCURACY: {best_accuracy:.1f}%")
else:
    print("No improvement found")
print("=" * 80)