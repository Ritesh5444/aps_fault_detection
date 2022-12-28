
# Provide the mongodb localhost url to connect python to mongodb.
#client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

#This is a test program written to check Sensor and exception modules written 
import sys,os
from sensor.exception import SensorException
from sensor.logger import logging


def sensor_and_exception():
     try:
          logging.info("Starting the test logger and exception")
          result = 3/0
          print (result)
          logging.info("Stopping the test logger and exception")
     except Exception as e:
          logging.info("Stopping the test logger and exception")
          raise SensorException(e, sys)

          
if __name__ == "__main__":
     try:
          sensor_and_exception()
     except Exception as e:
          print(e)

     