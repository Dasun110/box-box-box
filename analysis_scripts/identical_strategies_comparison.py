import json

races = json.load(open('../data/historical_races/races_00000-00999.json'))

# Find races with drivers using identical strategies
# They should have near-identical times if our model is correct

print("=" * 80)
print("DRIVERS WITH IDENTICAL STRATEGIES (same tire, same pit lap)")
print("=" * 80)

count = 0
for race in races[:200]:
    config = race['race_config']
    strategies_dict = {}

    # Group drivers by strategy
    for pos in range(1, 21):
        strategy = race['strategies'][f'pos{pos}']
        driver_id = strategy['driver_id']

        # Create strategy signature
        tire_sequence = [strategy['starting_tire']]
        for pit in strategy['pit_stops']:
            tire_sequence.append(pit['to_tire'])

        pit_laps = tuple(p['lap'] for p in strategy['pit_stops'])
        strategy_sig = (tuple(tire_sequence), pit_laps)

        if strategy_sig not in strategies_dict:
            strategies_dict[strategy_sig] = []
        strategies_dict[strategy_sig].append(driver_id)

    # Find strategies with 2+ drivers
    for strategy_sig, drivers in strategies_dict.items():
        if len(drivers) > 1:
            finishing_order = race['finishing_positions']
            positions = [finishing_order.index(d) + 1 for d in drivers]

            tire_seq, pit_laps = strategy_sig

            print(f"\n{race['race_id']} - {config['track']} ({config['track_temp']}°C)")
            print(f"  Strategy: {' → '.join(tire_seq)}, pits at laps {pit_laps}")
            print(f"  Drivers: {', '.join(drivers)}")
            print(f"  Finishing positions: {positions}")
            print(f"  Position spread: {max(positions) - min(positions)} places")

            count += 1
            if count > 10:
                break

    if count > 10:
        break

print(f"\nTotal matching strategies found: {count}")