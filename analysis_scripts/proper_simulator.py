import json


class RaceSimulator:
    """Proper F1 race simulator with best discovered formula"""

    def __init__(self):
        # Best config from our analysis
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
        """
        Simulate a race and return finishing positions
        """
        total_laps = race_config['total_laps']
        base_lap_time = race_config['base_lap_time']
        pit_lane_time = race_config['pit_lane_time']

        driver_times = {}

        # For each driver (pos1 through pos20)
        for pos in range(1, 21):
            pos_key = f'pos{pos}'
            strategy = strategies[pos_key]
            driver_id = strategy['driver_id']

            total_time = 0
            current_tire = strategy['starting_tire']
            tire_age = 0
            pit_index = 0

            # Simulate lap by lap
            for lap in range(1, total_laps + 1):
                # Check for pit stop at end of this lap
                if pit_index < len(strategy['pit_stops']):
                    pit_stop = strategy['pit_stops'][pit_index]
                    if lap == pit_stop['lap']:
                        # Driver pits
                        total_time += pit_lane_time
                        current_tire = pit_stop['to_tire']
                        tire_age = 0
                        pit_index += 1

                # Increment tire age at start of lap
                tire_age += 1

                # Calculate lap time
                tire_offset = self.tire_offsets[current_tire]
                degradation = self.tire_degradation[current_tire] * tire_age
                lap_time = base_lap_time + tire_offset + degradation

                total_time += lap_time

            driver_times[driver_id] = total_time

        # Sort by time and return order
        sorted_drivers = sorted(driver_times.items(), key=lambda x: x[1])
        finishing_positions = [driver_id for driver_id, time in sorted_drivers]

        return finishing_positions

    def test_on_race(self, race):
        """Test simulator on a single race"""
        predicted = self.simulate_race(race['race_config'], race['strategies'])
        actual = race['finishing_positions']

        matches = sum(1 for p, a in zip(predicted, actual) if p == a)

        return {
            'predicted': predicted,
            'actual': actual,
            'matches': matches,
            'accuracy': matches / 20
        }


# Test on all 1000 races
races = json.load(open('../data/historical_races/races_00000-00999.json'))
simulator = RaceSimulator()

print("=" * 80)
print("SIMULATOR VALIDATION: Testing on all 1000 races")
print("=" * 80)

total_matches = 0
total_races = len(races)

for race_idx, race in enumerate(races):
    result = simulator.test_on_race(race)
    total_matches += result['matches']

    if (race_idx + 1) % 100 == 0:
        current_accuracy = total_matches / ((race_idx + 1) * 20) * 100
        print(f"Processed {race_idx + 1} races: {current_accuracy:.1f}% accuracy so far")

final_accuracy = total_matches / (total_races * 20) * 100

print("\n" + "=" * 80)
print(f"FINAL RESULTS ON 1000 RACES")
print(f"Total matches: {total_matches} out of {total_races * 20}")
print(f"Overall accuracy: {final_accuracy:.1f}%")
print("=" * 80)