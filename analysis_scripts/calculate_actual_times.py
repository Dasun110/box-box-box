import json


def calculate_driver_time(race, driver_id):
    """
    Calculate a driver's total race time
    We need to figure this out from position and other clues
    """
    config = race['race_config']
    total_laps = config['total_laps']
    base_lap_time = config['base_lap_time']
    pit_lane_time = config['pit_lane_time']

    # Find driver's strategy
    strategy = None
    for pos in range(1, 21):
        if race['strategies'][f'pos{pos}']['driver_id'] == driver_id:
            strategy = race['strategies'][f'pos{pos}']
            break

    if not strategy:
        return None

    # Find finishing position
    finishing_order = race['finishing_positions']
    finishing_pos = finishing_order.index(driver_id)

    return {
        'driver_id': driver_id,
        'finishing_pos': finishing_pos,
        'starting_tire': strategy['starting_tire'],
        'pit_stops': len(strategy['pit_stops']),
        'pit_details': strategy['pit_stops']
    }


races = json.load(open('../data/historical_races/races_00000-00999.json'))
race = races[0]

print("=" * 60)
print(f"RACE: {race['race_id']} - {race['race_config']['track']}")
print("=" * 60)
print(f"Base lap time: {race['race_config']['base_lap_time']}")
print(f"Total laps: {race['race_config']['total_laps']}")
print(f"Pit penalty: {race['race_config']['pit_lane_time']}")
print(f"Track temp: {race['race_config']['track_temp']}°C")

print("\n=== TOP 5 FINISHERS ===")
for i in range(5):
    driver_id = race['finishing_positions'][i]
    info = calculate_driver_time(race, driver_id)
    print(f"\n{i + 1}. {driver_id}")
    print(f"   Starting tire: {info['starting_tire']}")
    print(f"   Pit stops: {info['pit_stops']}")
    for pit in info['pit_details']:
        print(f"     Lap {pit['lap']}: {pit['from_tire']} → {pit['to_tire']}")

print("\n=== BOTTOM 5 FINISHERS ===")
for i in range(15, 20):
    driver_id = race['finishing_positions'][i]
    info = calculate_driver_time(race, driver_id)
    print(f"\n{i + 1}. {driver_id}")
    print(f"   Starting tire: {info['starting_tire']}")
    print(f"   Pit stops: {info['pit_stops']}")
    for pit in info['pit_details']:
        print(f"     Lap {pit['lap']}: {pit['from_tire']} → {pit['to_tire']}")