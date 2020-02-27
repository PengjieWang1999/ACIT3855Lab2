from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Temperature(Base):
    """ Temperature """

    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    device_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    high = Column(Integer, nullable=False)
    low = Column(Integer, nullable=False)

    def __init__(self, user_id, device_id, timestamp, high, low):
        """ Initializes a temperature reading """
        self.user_id = user_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.high = high
        self.low = low

    def to_dict(self):
        """ Dictionary Representation of a temperature reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['device_id'] = self.device_id
        dict['date_created'] = self.date_created.strftime("%Y-%m-%dT%H:%M:%S")
        dict['temperature'] = {}
        dict['temperature']['high'] = self.high
        dict['temperature']['low'] = self.low
        dict['timestamp'] = self.timestamp

        return dict
