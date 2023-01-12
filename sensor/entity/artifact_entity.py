#Artifact  - Output

from dataclasses import dataclass

@dataclass
class DataIngestionAtrifact:
    feature_store_file_path : str
    train_file_path: str
    test_file_path : str
    
@dataclass
class DataValidationArtifact:
    report_file_path: str


    
class DataTransformationAtrifact:...
class ModelTrainerArtifact:...
class ModelEvaluationArtifact:...
class ModelPusherArtifact:...
