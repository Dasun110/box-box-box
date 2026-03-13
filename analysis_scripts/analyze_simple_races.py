import json
import statistics

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Find races where at least one driver has no pit stops
simple_races = []

for race in races:
    for pos in range(1, 21):
        pos_key = f'pos{pos}'
        strategy = race['strategies'][pos_key]

        # If no pit stops, this is a simple race
        if len(strategy['pit_stops']) == 0:
            simple_races.append({
                'race': race,
                'pos': pos_key,
                'strategy': strategy
            })

print(f"Found {len(simple_races)} drivers with no pit stops")
print(f"\nFirst 5 simple races:")
for i, item in enumerate(simple_races[:5]):
    race = item['race']
    strat = item['strategy']
    print(f"\n{i + 1}. Race {race['race_id']}, {item['pos']}")
    print(f"   Driver: {strat['driver_id']}")
    print(f"   Tire: {strat['starting_tire']}")
    print(f"   Track: {race['race_config']['track']}")
    print(f"   Base lap time: {race['race_config']['base_lap_time']}")
    print(f"   Temperature: {race['race_config']['track_temp']}")