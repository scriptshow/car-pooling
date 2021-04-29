FROM python:3.7-alpine

ENV CAR_POOLING_LOG_LEVEL 'info'

# Copying all the files needed
RUN mkdir -p /car-pooling
WORKDIR /car-pooling
ADD ./ /car-pooling/

# Setting permissions to be executed
RUN chmod +x gunicorn_starter.sh

# Installing all python dependences
RUN pip install -r requirements.txt

EXPOSE 9091

ENTRYPOINT ["./gunicorn_starter.sh"]
