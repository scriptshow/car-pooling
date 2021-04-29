from shared.config import MIN_CAR_SEATS, MAX_CAR_SEATS, MIN_JOURNEY_SIZE, MAX_JOURNEY_SIZE


def validate_car_list(car_list):
    """
    Function to validate a list of cars.

    :param car_list: List of cars
    :return: True or False, depending if passing the validation
    """
    result = True
    car_ids = set()
    try:
        for car in car_list:
            if 'id' in car and 'seats' in car:
                if 0 < car['id']:
                    if MIN_CAR_SEATS <= car['seats'] <= MAX_CAR_SEATS:
                        if car['id'] in car_ids:
                            result = False
                            break
                        else:
                            car_ids.add(car['id'])
                    else:
                        result = False
                        break
                else:
                    result = False
                    break
            else:
                result = False
                break

    except TypeError:
        result = False

    return result


def validate_journey(journey):
    """
    Function to validate a journey.

    :param journey: dictionary with journey information
    :return: True or False, depending if passing the validation
    """
    result = True
    try:
        if 'id' in journey and 'people' in journey:
            if MIN_JOURNEY_SIZE <= journey['people'] <= MAX_JOURNEY_SIZE:
                if not type(journey['id']) is int:
                    result = False
            else:
                result = False
        else:
            result = False
    except TypeError:
        result = False

    return result


def validate_form(form):
    """
    Function to validate a form data.

    :param form: dictionary with form data
    :return: True or False, depending if passing the validation
    """
    result = True
    if 'ID' not in form:
        return False
    else:
        if not int(form['ID']) > 0:
            return False

    return result
