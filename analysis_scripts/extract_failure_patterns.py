import json
from collections import defaultdict


class RaceSimulator:
    def __init__(self):
        self.tire_offsets = {
            'SOFT': 0.05,
            'MEDIUM': 0.0,
            'HARD': -0.10
        }
        self.tire_degradation = {
            'SOFT': 0.10,
            'MEDIUM': 0.05,
            'HARD': 0.03
        }

    def simulate_race(self, race_config, strategies):
        total_laps = race_config['total_laps']
        base_lap_time = race_config['base_lap_time']
        pit_lane_time = race_config['pit_lane_time']

        driver_times = {}

        for pos in range(1, 21):
            strategy = strategies[f'pos{pos}']
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
                tire_offset = self.tire_offsets[current_tire]
                degradation = self.tire_degradation[current_tire] * tire_age
                lap_time = base_lap_time + tire_offset + degradation
                total_time += lap_time

            driver_times[driver_id] = total_time

        sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
        return [driver_id for driver_id, time in sorted_drivers], driver_times


races = json.load(open('../data/historical_races/races_00000-00999.json'))
simulator = RaceSimulator()

print("=" * 80)
print("PATTERN ANALYSIS: Where We Get Things Wrong")
print("=" * 80)

# Analyze what causes prediction errors
error_patterns = {
    'tracks': defaultdict(int),
    'temperatures': defaultdict(int),
    'grid_positions': defaultdict(int)
}

correct_by_track = defaultdict(list)
error_by_track = defaultdict(list)

for race in races:
    predicted, driver_times = simulator.simulate_race(race['race_config'], race['strategies'])
    actual = race['finishing_positions']

    track = race['race_config']['track']
    temp = race['race_config']['track_temp']

    matches = sum(1 for p, a in zip(predicted, actual) if p == a)
    accuracy = matches / 20

    correct_by_track[track].append(accuracy)

    # Analyze where errors occur
    for pos in range(20):
        if predicted[pos] != actual[pos]:
            error_patterns['tracks'][track] += 1
            error_patterns['temperatures'][temp] += 1
            error_patterns['grid_positions'][pos] += 1

print("\nAccuracy by Track:")
for track in sorted(correct_by_track.keys()):
    accuracies = correct_by_track[track]
    avg_acc = sum(accuracies) / len(accuracies) * 100
    print(f"  {track:15s}: {avg_acc:5.1f}%")

print("\nError Count by Temperature:")
for temp in sorted(error_patterns['temperatures'].keys()):
    print(f"  {temp:2d}°C: {error_patterns['temperatures'][temp]:4d} errors")

print("\nError Count by Grid Position (where we got prediction wrong):")
for pos in range(20):
    print(f"  Position {pos + 1:2d} (grid pos {pos + 1:2d}): {error_patterns['grid_positions'][pos]:4d} errors")