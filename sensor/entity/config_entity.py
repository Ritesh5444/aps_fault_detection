#Confifuration - input
import os
from datetime import datetime

FILE_NAME = 'sensor.csv'
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = 'test.csv'

class TrainingPipelineConfig:

    def __init__(self):
        #This will create a folder name artifact everytime training pipeline is executed. 
        # And under that Artifact name folder there will be subfolder with datetime stamp
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%y__%H%M%S')}")

class DataIngestionConfig:
    
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:

    #training_pipeline_config: TrainingPipelineConfig - it is creating object of 
    # TrainingPipelineConfig class and we are accessing 'artifact_dir' using this object
            self.database_name = "aps"
            self.collection_name = "sensor"
            #This will create data ingestion folder when traning pipeline is executed under the datetime folder created above
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store")
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            raise SensorException(e,sys)


    def to_dict(self,) -> dict:
        try:
            return self.__dict__ 
        except Exception as e:

            raise SensorException(e,sys) 

class DataValidationConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig()):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data validation")
        self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
        self.missing_threshold: float = 0.2
        self.base_file_path = os.path.join("aps_failure_training_set1")


class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
