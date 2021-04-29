from os import getenv

# Logging configuration variables
LOG_LEVEL_ALLOWED = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG_LEVEL = getenv('CAR_POOLING_LOG_LEVEL', 'INFO').upper()

# Car default values
MIN_CAR_SEATS = 4
MAX_CAR_SEATS = 6

# Journey default values
MIN_JOURNEY_SIZE = 1
MAX_JOURNEY_SIZE = 6
