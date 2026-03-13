import json


def simulate_with_degradation_curve(race, degradation_func):
    """
    Test a specific degradation function
    degradation_func: function(tire_age) -> time_penalty
    """
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

            # Calculate lap time with degradation function
            # Assume tire compound has ZERO offset (all same speed)
            degradation = degradation_func(tire_age)
            lap_time = base_lap_time + degradation

            total_time += lap_time

        driver_times[driver_id] = total_time

    # Check accuracy
    sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
    predicted = [d for d, t in sorted_drivers]
    actual = race['finishing_positions']

    matches = sum(1 for p, a in zip(predicted, actual) if p == a)
    return matches / 20 * 100


races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Define different degradation curves
degradation_curves = {
    'None': lambda age: 0,
    'Linear 0.01': lambda age: age * 0.01,
    'Linear 0.05': lambda age: age * 0.05,
    'Linear 0.1': lambda age: age * 0.1,
    'Linear 0.2': lambda age: age * 0.2,
    'Quadratic 0.001': lambda age: (age ** 2) * 0.001,
    'Quadratic 0.005': lambda age: (age ** 2) * 0.005,
    'Exponential 1.001': lambda age: (1.001 ** age) - 1,
    'Exponential 1.002': lambda age: (1.002 ** age) - 1,
    'Stepped (slow 1-5, fast 6+)': lambda age: 0 if age <= 5 else (age - 5) * 0.1,
    'Stepped (slow 1-10, fast 11+)': lambda age: 0 if age <= 10 else (age - 10) * 0.05,
}

print("=" * 70)
print("TESTING DIFFERENT DEGRADATION CURVES")
print("=" * 70)

best_accuracy = 0
best_curve = None

for curve_name, curve_func in degradation_curves.items():
    total_accuracy = 0
    races_tested = min(50, len(races))

    for race in races[:races_tested]:
        accuracy = simulate_with_degradation_curve(race, curve_func)
        total_accuracy += accuracy

    avg_accuracy = total_accuracy / races_tested

    print(f"{curve_name:35s} → {avg_accuracy:5.1f}%")

    if avg_accuracy > best_accuracy:
        best_accuracy = avg_accuracy
        best_curve = curve_name

print("\n" + "=" * 70)
print(f"BEST CURVE: {best_curve}")
print(f"ACCURACY: {best_accuracy:.1f}%")
print("=" * 70)