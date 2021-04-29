from flask_restful import Resource
from flask import request
import logging
from models.journey import JourneyModel
from models.car import CarModel
from shared.validators import validate_journey, validate_form


class JourneyResource(Resource):
    """
    Journey resource, will manage all the API operations related with journey operations.
    """

    def post(self):
        """
        Function to add a new journey to the system.

        :return:
            200 OK When the group is registered correctly
            400 Bad Request When there is a failure in the request format or the payload can't be unmarshalled.
        """
        response = None
        json_data = request.get_json()
        logging.info("Adding new journey: ({0})".format(str(json_data)))
        if validate_journey(json_data):
            if not JourneyModel.check_if_exists(json_data['id']):
                journey = JourneyModel(journey_id=json_data['id'], people=json_data['people'])
                logging.debug("Searching for a free car jor journey ...")
                car_found = CarModel.search_for_free_seats(journey.get_people())
                if car_found:
                    car_found.book_seats(journey.get_people())
                    journey.assign_car(car_found)
                    logging.debug("Journey has been asigned to car: ({0})".format(car_found))
                else:
                    logging.debug("No car found, journey will be added to the waiting list.")
                journey.create()
                logging.info("Journey has been created.")
                http_code = 200
            else:
                logging.error("Journey already exists.")
                http_code = 400
        else:
            logging.error("Journey has not a valid format.")
            http_code = 400

        return response, http_code


class DropOffResource(Resource):
    """
    DropOff resource, will manage all the API operations where dropoff are done.
    """

    def post(self):
        """
        Function to make a dropoff for a current journey.

        :return:
            200 OK When the group is unregistered correctly.
            404 Not Found When the group is not to be found.
            400 Bad Request When there is a failure in the request format or the payload can't be unmarshalled.
        """
        response = None
        json_data = request.form
        logging.info("DropOff call for journey: ({0})".format(str(json_data)))
        if validate_form(json_data):
            journey_id = int(json_data['ID'])
            journey = JourneyModel.get_journey_by_id(journey_id)
            if journey:
                logging.debug("Journey has been found: ({0})".format(journey))
                car = journey.get_assigned_car()
                if car:
                    logging.debug("Journey is already sit in a car: ({0})".format(car))
                    if car.release_seats(journey.get_people()):
                        logging.debug("Seats have been released from the car. Looking for a new group to ride in.")
                        while car.get_free_seats() > 0:
                            new_journey = JourneyModel.get_next_waiting(car.get_free_seats())
                            if new_journey:
                                logging.debug("New journey found to ride in the car: ({0})".format(new_journey))
                                if car.book_seats(new_journey.get_people()):
                                    new_journey.assign_car(car)
                                    new_journey.remove_from_unassigned_journeys()
                                    logging.debug("New journey has been assigned to the car.")
                            else:
                                break  # if no more journeys found, leave the seats free
                        http_code = 200
                    else:
                        logging.error("Seats were not able to be released.")
                        http_code = 500
                else:
                    logging.debug("Journey had not a car assigned.")
                    http_code = 200
                journey.delete()
                logging.info("Journey has been dropped off.")
            else:
                logging.warning("Journey with id: ({0}), not found.".format(journey_id))
                http_code = 404
        else:
            logging.error("Form has not a valid format.")
            http_code = 400

        return response, http_code


class LocateResource(Resource):
    """
    Locate resource, will manage all the API operations to retrieve information about the journeys.
    """

    def post(self):
        """
        Function to retrieve the assigned car for a specific journey, if already assigned.

        :return:
            200 OK With the car as the payload when the group is assigned to a car.
            204 No Content When the group is waiting to be assigned to a car.
            404 Not Found When the group is not to be found.
            400 Bad Request When there is a failure in the request format or the payload can't be unmarshalled.
        """
        response = None
        json_data = request.form
        logging.info("Locate request for journey: ({0})".format(str(json_data)))
        if validate_form(json_data):
            journey_id = int(json_data['ID'])
            journey = JourneyModel.get_journey_by_id(journey_id)
            if journey:
                logging.debug("Journey has been found: ({0})".format(journey))
                car = journey.get_assigned_car()
                if car:
                    logging.info("Car found: ({0}) for journey: ({1}).".format(car, journey))
                    http_code = 200
                    response = car.to_json()
                else:
                    logging.info("Journey has not a car assigned yet, still waiting.")
                    http_code = 204
            else:
                logging.warning("Journey with id: ({0}), not found.".format(journey_id))
                http_code = 404
        else:
            logging.error("Form has not a valid format.")
            http_code = 400

        return response, http_code
