from flask import Flask, make_response, Response
from flask_restful import Api
from shared.database import db
from shared.config import LOG_LEVEL, LOG_LEVEL_ALLOWED
from resources.status import StatusResource
from resources.car import CarResource
from resources.journey import JourneyResource, DropOffResource, LocateResource
from logging.config import dictConfig
import json

if LOG_LEVEL not in LOG_LEVEL_ALLOWED:
    LOG_LEVEL = 'INFO'

# Default logging configuration
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['wsgi']
    }
})

# Flask configuration
app = Flask(__name__)

# Initialize database
db.init_db()

# API configuration
api = Api(app)
api.add_resource(StatusResource, '/status')
api.add_resource(CarResource, '/cars')
api.add_resource(JourneyResource, '/journey')
api.add_resource(DropOffResource, '/dropoff')
api.add_resource(LocateResource, '/locate')


# Default output for all the request in the API
@api.representation('application/json')
def output_json(data, code, headers=None):
    if data:
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
    else:
        resp = Response(status=code)
    return resp


if __name__ == '__main__':
    app.run()
