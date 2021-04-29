# Car Pooling Service

Design/implement a system to manage car pooling.

We provide the service of taking people from point A to point B.
So far we have done it without sharing cars with multiple groups of people.
This is an opportunity to optimize the use of resources by introducing car
pooling.

You have been assigned to build the car availability service that will be used
to track the available seats in cars.

Cars have a different amount of seats available, they can accommodate groups of
up to 4, 5 or 6 people.

People requests cars in groups of 1 to 6. People in the same group want to ride
on the same car. You can take any group at any car that has enough empty seats
for them. If it's not possible to accommodate them, they're willing to wait until 
there's a car available for them. Once a car is available for a group
that is waiting, they should ride. 

Once they get a car assigned, they will journey until the drop off, you cannot
ask them to take another car (i.e. you cannot swap them to another car to
make space for another group).

In terms of fairness of trip order: groups should be served as fast as possible,
but the arrival order should be kept when possible.
If group B arrives later than group A, it can only be served before group A
if no car can serve group A.

For example: a group of 6 is waiting for a car and there are 4 empty seats at
a car for 6; if a group of 2 requests a car you may take them in the car.
This may mean that the group of 6 waits a long time,
possibly until they become frustrated and leave.

## Evaluation rules

This challenge has a partially automated scoring system. This means that before
it is seen by the evaluators, it needs to pass a series of automated checks
and scoring.

## API

This service must provide a REST API which will be used to interact with it.

This API must comply with the following contract:

### GET /status

Indicate the service has started up correctly and is ready to accept requests.

Responses:

* **200 OK** When the service is ready to receive requests.

### PUT /cars

Load the list of available cars in the service and remove all previous data
(existing journeys and cars). This method may be called more than once during 
the life cycle of the service.

**Body** _required_ The list of cars to load.

**Content Type** `application/json`

Sample:

```json
[
  {
    "id": 1,
    "seats": 4
  },
  {
    "id": 2,
    "seats": 6
  }
]
```

Responses:

* **200 OK** When the list is registered correctly.
* **400 Bad Request** When there is a failure in the request format, expected
  headers, or the payload can't be unmarshalled.

### POST /journey

A group of people requests to perform a journey.

**Body** _required_ The group of people that wants to perform the journey

**Content Type** `application/json`

Sample:

```json
{
  "id": 1,
  "people": 4
}
```

Responses:

* **200 OK** or **202 Accepted** When the group is registered correctly
* **400 Bad Request** When there is a failure in the request format or the
  payload can't be unmarshalled.

### POST /dropoff

A group of people requests to be dropped off. Whether they traveled or not.

**Body** _required_ A form with the group ID, such that `ID=X`

**Content Type** `application/x-www-form-urlencoded`

Responses:

* **200 OK** or **204 No Content** When the group is unregistered correctly.
* **404 Not Found** When the group is not to be found.
* **400 Bad Request** When there is a failure in the request format or the
  payload can't be unmarshalled.

### POST /locate

Given a group ID such that `ID=X`, return the car the group is traveling
with, or no car if they are still waiting to be served.

**Body** _required_ A url encoded form with the group ID such that `ID=X`

**Content Type** `application/x-www-form-urlencoded`

**Accept** `application/json`

Responses:

* **200 OK** With the car as the payload when the group is assigned to a car.
* **204 No Content** When the group is waiting to be assigned to a car.
* **404 Not Found** When the group is not to be found.
* **400 Bad Request** When there is a failure in the request format or the
  payload can't be unmarshalled.
  
## Requirements

:warning: The project needs to be self-contained without using a database.

- The service should be as efficient as possible.
  It should be able to work reasonably well with at least $`10^4`$ / $`10^5`$ cars / waiting groups.
  Explain how you did achieve this requirement.
- You are free to modify the repository as much as necessary to include or remove
  dependencies, subject to tooling limitations above.
- Document your decisions using MRs or in this very README adding sections to it,
  the same way you would be generating documentation for any other deliverable.
  We want to see how you operate in a quasi real work environment.

_____________________________________________________________________________________________________________

# Documentation

In this section, will be available all the documentation related with the solution.

## Programming language

I chose the Python programming language to do this application because this one works very
well with web development (API Rest in this case), and it's very fast to develop a prototype.
Python language has as well a very good syntax and is very easy to read and understand the code.

## Framework

I chose the Flask framework to build this application because it's a very small application that 
doesn't need many of the features given by others heavy frameworks like Django.

I added as well the gunicorn usage to serve the application, just to make it more stable with a 
high number of requests.

## Database

As the application must be self-contained, I decided to build my own "database", 
it's not a database itself, but it tries to simulate it. It's a class that give a
high level operations to be used by the other models.

I created as well two models, car and journey, simulating two tables in a database.

## Performance

To reach the performance needs: 
- All the storage in database model is based in dictionaries (key, value), by this way, when looking
  for a specific id, it will be very fast because will be looking only the value for id key specified, 
  without impacting in the time to search it the size of the dictionary.
  We have three different dictionaries:
  - Cars dictionary, where we store all the cars created.
  - Journeys dictionary, where we store all the journeys created.
  - Available Cars dictionary, this dictionary is quite different, this use as key the possible number
    of seats available in a car (from 1 to 6, in this project), and as value, it's using a list of cars 
    matching this number of seats available.
- In addition to the dictionary-based models in the database storage, we have one list, used as queue
  for the journeys that are waiting and have not been assigned to a car yet. We are using a list because
  we will do only operations to get the first value or append to the last one, the lists are very fast 
  for that, and keeps the input order.
- The storage system is based in pointers. We will be managing only CarModel's and JourneyModel's,
  which will be created with the classes proposed in model folder. Doing this, the memory used
  to manage all the "in memory" instances will be as lightweight as possible. We will have only one instance
  created for each car/journey, but will be accessible and modifiable by all the dictionaries.
- Gunicorn is serving only one worker, due the dependence of sharing the "in memory" database.
- As we are using only one worker, we will work only with one thread, as Python is faster monothread due the GIL
  
## Project Structure

Main project file is: "app.py", this file includes the variables initialization and all the endpoint routes.

- Models folder, includes all the models used in the project.
- Resources folder, includes all the classes which manage the endpoint requests.
- Shared folder, includes all the objects/functions used by whole project from different places.
- Tests folder, includes all the unit testing.


