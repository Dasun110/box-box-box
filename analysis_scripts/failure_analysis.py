import json


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
            pos_key = f'pos{pos}'
            strategy = strategies[pos_key]
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
        return [driver_id for driver_id, time in sorted_drivers]


races = json.load(open('../data/historical_races/races_00000-00999.json'))
simulator = RaceSimulator()

print("=" * 80)
print("DETAILED FAILURE ANALYSIS")
print("=" * 80)

# Find races where we got MOST wrong
worst_races = []

for race in races:
    predicted = simulator.simulate_race(race['race_config'], race['strategies'])
    actual = race['finishing_positions']

    matches = sum(1 for p, a in zip(predicted, actual) if p == a)
    worst_races.append({
        'race_id': race['race_id'],
        'track': race['race_config']['track'],
        'temp': race['race_config']['track_temp'],
        'matches': matches,
        'predicted': predicted,
        'actual': actual
    })

worst_races.sort(key=lambda x: x['matches'])

print("\n10 WORST PREDICTIONS:")
for i, race_result in enumerate(worst_races[:10], 1):
    print(f"\n{i}. {race_result['race_id']} - {race_result['track']} ({race_result['temp']}°C)")
    print(f"   Correct: {race_result['matches']}/20")
    print(f"   Predicted top 5: {race_result['predicted'][:5]}")
    print(f"   Actual top 5:    {race_result['actual'][:5]}")

print("\n" + "=" * 80)
print("\n10 BEST PREDICTIONS:")
best_races = sorted(worst_races, key=lambda x: x['matches'], reverse=True)
for i, race_result in enumerate(best_races[:10], 1):
    print(f"\n{i}. {race_result['race_id']} - {race_result['track']} ({race_result['temp']}°C)")
    print(f"   Correct: {race_result['matches']}/20")