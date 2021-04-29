from flask_restful import Resource
import logging


class StatusResource(Resource):
    """
    Status resource, will manage all the API operations related with Cabify system status.
    """

    def get(self):
        """
        This function just return HTTP 200 code, to verify that system is up and running.

        :return: HTTP code 200, always.
        """
        logging.info("Status request received, system is up and running.")
        http_code = 200
        response = None

        return response, http_code
