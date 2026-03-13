import json


def analyze_degradation(races, tire_compound, start_offset):
    """
    Analyze how a specific tire compound degrades
    """

    # Find races where drivers start with this tire and don't pit
    lap_times_by_age = {}

    for race in races:
        config = race['race_config']
        base_lap_time = config['base_lap_time']
        total_laps = config['total_laps']

        for pos in range(1, 21):
            pos_key = f'pos{pos}'
            strategy = race['strategies'][pos_key]

            # Only look at drivers using this tire with no pit stops
            if (strategy['starting_tire'] == tire_compound and
                    len(strategy['pit_stops']) == 0):

                # For this driver:
                # - Lap 1 is at tire age 1
                # - Lap 2 is at tire age 2
                # - etc

                # Record in lap_times_by_age
                if total_laps not in lap_times_by_age:
                    lap_times_by_age[total_laps] = {}

                for age in range(1, min(10, total_laps + 1)):
                    if age not in lap_times_by_age[total_laps]:
                        lap_times_by_age[total_laps][age] = []

                    # The lap time at age X is:
                    # base_lap_time + tire_offset + degradation_penalty
                    # We can estimate degradation by looking at differences

                    lap_times_by_age[total_laps][age].append({
                        'race_id': race['race_id'],
                        'track': config['track'],
                        'base_lap_time': base_lap_time,
                        'track_temp': config['track_temp']
                    })

    print(f"=== DEGRADATION ANALYSIS: {tire_compound} ===")
    print(f"Start offset (assumption): {start_offset} seconds")
    print(f"\nData points by tire age:")
    for laps in sorted(lap_times_by_age.keys()):
        print(f"\n{laps} lap race:")
        for age in sorted(lap_times_by_age[laps].keys()):
            count = len(lap_times_by_age[laps][age])
            print(f"  Age {age}: {count} drivers")


races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Analyze each compound
analyze_degradation(races, 'SOFT', -2.0)
analyze_degradation(races, 'MEDIUM', 0.0)
analyze_degradation(races, 'HARD', 2.0)