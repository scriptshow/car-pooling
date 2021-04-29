from shared.database import db


class JourneyModel(object):
    """
    Model used to store the Cabify journey.
        - All the journeys have his own identifier, the people traveling with and the assigned car if any.
    """
    id = None
    people = None
    car = None

    def __init__(self, journey_id, people):
        self.id = journey_id
        self.people = people

    def get_id(self):
        return self.id

    def get_people(self):
        return self.people

    def get_assigned_car(self):
        return self.car

    def create(self):
        db.add_journey(self)
        if not self.get_assigned_car():
            self.add_to_unassigned_journeys()
        return True

    def delete(self):
        db.delete_journey(self)
        if not self.get_assigned_car():
            self.remove_from_unassigned_journeys()
        return True

    def add_to_unassigned_journeys(self):
        db.add_to_unassigned_journeys(self)

    def remove_from_unassigned_journeys(self):
        db.remove_from_unassigned_journeys(self)

    def assign_car(self, car):
        self.car = car

    def to_json(self):
        return {'id': self.id, 'people': self.people, 'car': self.car}

    def __str__(self):
        return "id: {0}, people:{1}, car_assigned: ({2})".format(self.id, self.people, self.car)

    @staticmethod
    def get_journey_by_id(journey_id):
        return db.get_journey_by_id(journey_id)

    @staticmethod
    def check_if_exists(journey_id):
        return db.get_journey_by_id(journey_id)

    @staticmethod
    def get_next_waiting(available_seats):
        journey = db.get_next_journey(available_seats)
        return journey

