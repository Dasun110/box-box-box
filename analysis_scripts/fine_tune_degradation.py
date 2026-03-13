import json


def simulate_with_linear_deg(race, deg_rate):
    """Test linear degradation with specific rate"""
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
            degradation = deg_rate * tire_age
            lap_time = base_lap_time + degradation
            total_time += lap_time

        driver_times[driver_id] = total_time

    sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
    predicted = [d for d, t in sorted_drivers]
    actual = race['finishing_positions']

    matches = sum(1 for p, a in zip(predicted, actual) if p == a)
    return matches / 20 * 100


races = json.load(open('../data/historical_races/races_00000-00999.json'))

print("=" * 70)
print("FINE-TUNING LINEAR DEGRADATION RATE")
print("=" * 70)

best_accuracy = 0
best_rate = 0

# Try rates from 0.01 to 0.5
for deg_rate in [round(x * 0.01, 2) for x in range(1, 51)]:
    total_accuracy = 0
    races_tested = min(50, len(races))

    for race in races[:races_tested]:
        accuracy = simulate_with_linear_deg(race, deg_rate)
        total_accuracy += accuracy

    avg_accuracy = total_accuracy / races_tested

    print(f"Degradation rate {deg_rate:.2f} → {avg_accuracy:5.1f}%")

    if avg_accuracy > best_accuracy:
        best_accuracy = avg_accuracy
        best_rate = deg_rate

print("\n" + "=" * 70)
print(f"BEST DEGRADATION RATE: {best_rate:.2f} seconds/lap age")
print(f"ACCURACY: {best_accuracy:.1f}%")
print("=" * 70)