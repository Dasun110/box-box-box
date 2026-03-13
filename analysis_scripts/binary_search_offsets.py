import json
import itertools


def test_offsets(races, soft_offset, medium_offset, hard_offset):
    """Test a specific offset combination on all races"""
    tire_offsets = {
        'SOFT': soft_offset,
        'MEDIUM': medium_offset,
        'HARD': hard_offset
    }

    total_matches = 0
    total_drivers = 0

    for race in races[:100]:  # Test on first 100 races
        config = race['race_config']
        total_laps = config['total_laps']
        base_lap_time = config['base_lap_time']
        pit_lane_time = config['pit_lane_time']

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
                degradation = 0.05 * tire_age  # Try linear degradation
                lap_time = base_lap_time + tire_offset + degradation
                total_time += lap_time

            driver_times[driver_id] = total_time

        sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
        predicted = [d for d, t in sorted_drivers]
        actual = race['finishing_positions']

        matches = sum(1 for p, a in zip(predicted, actual) if p == a)
        total_matches += matches
        total_drivers += 20

    return total_matches / total_drivers * 100


races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Search grid
print("=" * 60)
print("GRID SEARCH FOR BEST OFFSETS")
print("=" * 60)

best_accuracy = 0
best_config = None

# Try different combinations
soft_values = [-2.0, -1.5, -1.0, -0.5, 0.0]
hard_values = [0.5, 1.0, 1.5, 2.0]

for soft_off in soft_values:
    for hard_off in hard_values:
        accuracy = test_offsets(races, soft_off, 0.0, hard_off)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_config = (soft_off, 0.0, hard_off)
            print(f"✅ New best: SOFT={soft_off}, MEDIUM=0.0, HARD={hard_off} → {accuracy:.1f}%")
        else:
            print(f"   SOFT={soft_off}, MEDIUM=0.0, HARD={hard_off} → {accuracy:.1f}%")

print("\n" + "=" * 60)
print(f"BEST CONFIG: SOFT={best_config[0]}, MEDIUM={best_config[1]}, HARD={best_config[2]}")
print(f"ACCURACY: {best_accuracy:.1f}%")
print("=" * 60)