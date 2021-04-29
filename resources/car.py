from flask_restful import Resource
from flask import request
import logging
from models.car import CarModel
from shared.validators import validate_car_list
from shared.database import db


class CarResource(Resource):
    """
    Car resource, will manage all the API operations related with Cabify cars.
    """

    def put(self):
        """
        Function to add a list of cars to the system, dropping all the current information (journeys included).
        :return: HTTP code, 200 if ok, 400 if not ok.
        """
        response = None
        json_data = request.get_json()
        logging.info("Updating the car list.")
        if validate_car_list(json_data):
            logging.debug("The car list is valid, cleaning all database entries ...")
            db.clean_database()
            for raw_car in json_data:
                car = CarModel(car_id=raw_car['id'], seats=raw_car['seats'])
                logging.debug("Creating car: ({0})".format(car))
                car.create()
            logging.info("Car list has been updated.")
            http_code = 200
        else:
            logging.error("Car list has not a valid format. ")
            http_code = 400

        return response, http_code
