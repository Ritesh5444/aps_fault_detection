import os

class TrainingPipelineConfig:

    def __init__(self):
        #This will create a folder name artifact everytime training pipeline is executed
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%y__%H%M%S')}")

class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
    #training_pipeline_config: TrainingPipelineConfig - it is creating object of 
    # TrainingPipelineConfig class and we are accessing 'artifact_dir' using this object
        self.database_name = "aps"
        self.collection_name = "sensor"
        #This will create data ingestion folder when traning pipeline is executed
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")

class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
