import connexion
from pykafka import KafkaClient
from threading import Thread
from connexion import NoContent
from flask_cors import CORS, cross_origin
import json
import logging
import logging.config

from sqlalchemy import and_

import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from temperature import Temperature
from humidity import Humidity
import datetime

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password']
                          + '@' + app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/'
                          + app_config['datastore']['db'])

DB_SESSION = sessionmaker(bind=DB_ENGINE)


'''def add_temperature(temperatureReading):
    """ Receives a temperature report """

    session = DB_SESSION()

    tp = Temperature(temperatureReading['user_id'],
                     temperatureReading['device_id'],
                     temperatureReading['timestamp'],
                     temperatureReading['temperature']['high'],
                     temperatureReading['temperature']['low'])

    session.add(tp)

    session.commit()
    session.close()

    return NoContent, 201'''


def get_temperature(startDate, endDate):
    """ Get temperature reports from the data store """

    results_list = []

    session = DB_SESSION()

    startDateTime = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")

    endDateTime = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")

    results = []

    results = (session.query(Temperature)
               .filter(and_(Temperature.date_created >= startDateTime.strftime("%Y-%m-%d %H:%M:%S"),
                            Temperature.date_created <= endDateTime.strftime("%Y-%m-%d %H:%M:%S"))))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()
    logger.debug("Temperature Events: " + str(results_list))

    return results_list, 200


'''def add_humidity(humidityReading):
    """ Add a humidity report to the data store """

    session = DB_SESSION()

    hd = Humidity(humidityReading['user_id'],
                  humidityReading['device_id'],
                  humidityReading['timestamp'],
                  humidityReading['humidity'])

    session.add(hd)

    session.commit()
    session.close()


    return NoContent, 201'''


def get_humidity(startDate, endDate):
    """ Get humidity reports from the data store """

    results_list = []
    startDateTime = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")

    endDateTime = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")

    session = DB_SESSION()

    results = (session.query(Humidity)
         .filter(and_(Humidity.date_created >= startDateTime.strftime("%Y-%m-%d %H:%M:%S"),
                      Humidity.date_created <= endDateTime.strftime("%Y-%m-%d %H:%M:%S"))))

    for result in results:
        results_list.append(result.to_dict())

    session.close()
    logger.debug("Humidity Events: " + str(results_list))

    return results_list, 200


def process_message():
    session = DB_SESSION()

    client = KafkaClient(hosts=app_config['datastore']['server'] + ':' + str(app_config['datastore']['port2']))
    topic = client.topics[app_config['datastore']['topic']]
    consumer = topic.get_simple_consumer(consumer_group='events', auto_commit_enable=True, auto_commit_interval_ms=100)

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg["type"] == "hd":
            msg = msg['payload']
            hd = Humidity(msg['user_id'],
                  msg['device_id'],
                  msg['timestamp'],
                  msg['humidity'])
            session.add(hd)
            session.commit()
            session.close()
        elif msg["type"] == "tp":
            msg = msg['payload']
            tp = Temperature(msg['user_id'],
                     msg['device_id'],
                     msg['timestamp'],
                     msg['temperature']['high'],
                     msg['temperature']['low'])
            session.add(tp)
            session.commit()
            session.close()
        else:
            print("None events data")


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    # run our standalone gevent server
    t1 = Thread(target=process_message)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
