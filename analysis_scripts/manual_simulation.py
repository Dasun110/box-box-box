import json
import math


def simulate_race_with_degradation(race, tire_offsets, degradation_rates, temp_effect):
    """
    Simulate race with degradation model

    tire_offsets: {'SOFT': -2.0, 'MEDIUM': 0.0, 'HARD': 2.0}
    degradation_rates: {'SOFT': 0.1, 'MEDIUM': 0.05, 'HARD': 0.02}
    temp_effect: function(temp) -> time_adjustment
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
            lap_time = base_lap_time

            # Add tire offset
            lap_time += tire_offsets.get(current_tire, 0)

            # Add degradation (increases with age)
            deg_rate = degradation_rates.get(current_tire, 0)
            degradation = deg_rate * tire_age  # Linear model
            lap_time += degradation

            # Add temperature effect
            lap_time += temp_effect(track_temp)

            total_time += lap_time

        driver_times[driver_id] = total_time

    # Sort and return order
    sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
    return [driver_id for driver_id, time in sorted_drivers]


# Test on first race
races = json.load(open('../data/historical_races/races_00000-00999.json'))
race = races[0]

# Try hypothesis
predicted = simulate_race_with_degradation(
    race,
    tire_offsets={'SOFT': -2.0, 'MEDIUM': 0.0, 'HARD': 2.0},
    degradation_rates={'SOFT': 0.05, 'MEDIUM': 0.02, 'HARD': 0.01},
    temp_effect=lambda t: (t - 20) * 0.01  # Higher temp slightly slower
)

actual = race['finishing_positions']

matches = sum(1 for p, a in zip(predicted, actual) if p == a)
print(f"Race: {race['race_id']}")
print(f"Match rate: {matches}/20 = {matches / 20 * 100:.0f}%")

# Print first few for visual inspection
print(f"\nFirst 10 places:")
print(f"Predicted: {predicted[:10]}")
print(f"Actual:    {actual[:10]}")