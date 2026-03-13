import sys
import json
import random

class RaceCar:
    def __init__(self, name, lap_time, tire_type, fuel_load):
        self.name = name
        self.lap_time = lap_time
        self.tire_type = tire_type
        self.fuel_load = fuel_load
        self.position = 0
        self.completed_laps = 0

    def simulate_lap(self, tire_degradation, tire_temperature):
        # Adjust lap time based on tire degradation and temperature
        adjusted_lap_time = self.lap_time + tire_degradation + tire_temperature
        # Adjust for fuel load
        adjusted_lap_time *= (self.fuel_load / 100)
        return adjusted_lap_time

class Race:
    def __init__(self, cars, laps):
        self.cars = cars
        self.laps = laps
        self.results = []

    def simulate_race(self):
        for lap in range(1, self.laps + 1):
            print(f"Simulating lap {lap}")
            for car in self.cars:
                tire_degradation = random.uniform(0, 2)
                tire_temperature = random.uniform(-1, 1)
                lap_time = car.simulate_lap(tire_degradation, tire_temperature)
                car.position += lap_time
                car.completed_laps += 1
            self.cars.sort(key=lambda x: x.position)
            self.results.append([(car.name, car.position) for car in self.cars])

    def predict_finishing_positions(self):
        final_positions = sorted(self.cars, key=lambda x: x.position)
        return {car.name: idx + 1 for idx, car in enumerate(final_positions)}

if __name__ == '__main__':
    input_data = json.load(sys.stdin)
    lap_count = input_data['laps']
    cars = [RaceCar(car['name'], car['lap_time'], car['tire_type'], car['fuel_load']) for car in input_data['cars']]
    race = Race(cars, lap_count)
    race.simulate_race()
    predictions = race.predict_finishing_positions()
    json.dump(predictions, sys.stdout)