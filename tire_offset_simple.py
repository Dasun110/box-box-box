import json
import numpy as np


def simulate_race_simple(race, tire_offsets):
    """
    Simulate a race with given tire offsets
    tire_offsets: dict with 'SOFT', 'MEDIUM', 'HARD' keys

    Returns: calculated finishing positions
    """
    config = race['race_config']
    total_laps = config['total_laps']
    base_lap_time = config['base_lap_time']
    pit_lane_time = config['pit_lane_time']

    driver_times = {}

    # For each driver (position)
    for pos in range(1, 21):
        pos_key = f'pos{pos}'
        strategy = race['strategies'][pos_key]
        driver_id = strategy['driver_id']

        total_time = 0
        current_tire = strategy['starting_tire']
        tire_age = 0
        pit_index = 0

        # Simulate lap by lap
        for lap in range(1, total_laps + 1):
            # Check if pit stop this lap
            if pit_index < len(strategy['pit_stops']):
                pit_stop = strategy['pit_stops'][pit_index]
                if lap == pit_stop['lap']:
                    # Apply pit penalty
                    total_time += pit_lane_time
                    # Change tire
                    current_tire = pit_stop['to_tire']
                    tire_age = 0
                    pit_index += 1

            # Increment tire age at START of lap
            tire_age += 1

            # Calculate lap time (NO DEGRADATION YET - SIMPLE MODEL)
            tire_offset = tire_offsets.get(current_tire, 0)
            lap_time = base_lap_time + tire_offset

            total_time += lap_time

        driver_times[driver_id] = total_time

    # Sort by time and return order
    sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
    finishing_order = [driver_id for driver_id, time in sorted_drivers]

    return finishing_order


# Test with different tire offsets
races = json.load(open('data/historical_races/races_00000-00999.json'))
race = races[0]

# Try to find tire offsets by trial and error
# SOFT should be fastest (negative offset)
# HARD should be slowest (positive offset)

test_offsets = {
    'SOFT': -2.0,  # 2 seconds faster
    'MEDIUM': 0.0,  # baseline
    'HARD': 2.0  # 2 seconds slower
}

predicted = simulate_race_simple(race, test_offsets)
actual = race['finishing_positions']

matches = sum(1 for p, a in zip(predicted, actual) if p == a)
print(f"Race: {race['race_id']}")
print(f"Matches: {matches}/20")
print(f"\nPredicted: {predicted[:5]}...")
print(f"Actual:    {actual[:5]}...")