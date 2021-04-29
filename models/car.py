from shared.database import db


class CarModel(object):
    """
    Model used to store the Cabify cars data
        - All the cars have his own identifier, the seats, and the available seats.
    """
    id = None
    seats = None
    seats_left = None

    def __init__(self, car_id, seats):
        self.id = car_id
        self.seats = seats
        self.seats_left = seats

    def get_id(self):
        return self.id

    def get_free_seats(self):
        return self.seats_left

    def create(self):
        db.add_car(self)
        return True

    def book_seats(self, seat_number):
        if seat_number <= self.seats_left:
            db.remove_from_available_cars(self)
            self.seats_left -= seat_number
            if self.seats_left > 0:
                db.add_to_available_cars(self)
            return True
        else:
            return False

    def release_seats(self, seat_number):
        if self.seats >= seat_number <= (self.seats - self.seats_left):
            if self.seats_left > 0:
                db.remove_from_available_cars(self)
            self.seats_left += seat_number
            db.add_to_available_cars(self)
            return True
        else:
            return False

    def to_json(self):
        return {'id': self.id, 'seats': self.seats, 'seats_left': self.seats_left}

    def __str__(self):
        return "id: {0}, seats:{1}, seats_left: {2}".format(self.id, self.seats, self.seats_left)

    @staticmethod
    def get_car_by_id(car_id):
        return db.get_car_by_id(car_id)

    @staticmethod
    def search_for_free_seats(seat_number):
        car_found = db.get_free_car_by_seats(seat_number)
        return car_found
