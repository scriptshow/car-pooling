from shared.config import MIN_JOURNEY_SIZE, MAX_JOURNEY_SIZE, MAX_CAR_SEATS


class Database(object):
    """
    Model used to simulate a database system, it will store all the live information on memory.
    """
    available_cars_by_seats = None
    unassigned_journeys = None
    cars = None
    journeys = None
    locked = True

    def __init__(self):
        self.locked = True

    def init_db(self):
        self.locked = False
        self.clean_database()

    def get_car_by_id(self, car_id):
        if car_id in self.cars:
            return self.cars[car_id]
        else:
            return None

    def get_journey_by_id(self, journey_id):
        if journey_id in self.journeys:
            return self.journeys[journey_id]
        else:
            return None

    def get_free_car_by_seats(self, seats_number):
        for number in range(seats_number, MAX_CAR_SEATS + 1):
            if self.available_cars_by_seats[number]:
                return self.available_cars_by_seats[number][0]
        return None

    def get_next_journey(self, available_seats):
        for journey in self.unassigned_journeys:
            if journey.get_people() <= available_seats:
                return journey
        return None

    def add_car(self, car):
        self.cars[car.get_id()] = car
        self.available_cars_by_seats[car.get_free_seats()].append(car)

    def add_journey(self, journey):
        self.journeys[journey.get_id()] = journey

    def add_to_available_cars(self, car):
        self.available_cars_by_seats[car.get_free_seats()].append(car)

    def clean_database(self):
        self.available_cars_by_seats = {number: [] for number in range(MIN_JOURNEY_SIZE, MAX_JOURNEY_SIZE + 1)}
        self.unassigned_journeys = []
        self.cars = {}
        self.journeys = {}

    def add_to_unassigned_journeys(self, journey):
        self.unassigned_journeys.append(journey)

    def remove_from_unassigned_journeys(self, journey):
        self.unassigned_journeys.remove(journey)

    def delete_journey(self, journey):
        self.journeys.pop(journey.get_id())

    def remove_from_available_cars(self, car):
        self.available_cars_by_seats[car.get_free_seats()].remove(car)
