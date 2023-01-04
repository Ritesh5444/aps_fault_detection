import sys,os
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.utils import get_collection_as_dataframe

if __name__ == "__main__":
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config= DataIngestionConfig(training_pipeline_config)
          print(data_ingestion_config.to_dict())
     except Exception as e:
          print(e)

