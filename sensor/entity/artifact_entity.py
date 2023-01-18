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


@dataclass
class DataTransformationAtrifact:
    transform_object_path : str
    transformed_train_path : str
    trannsformed_test_path : str
    target_encoder_path : str

class ModelTrainerArtifact:...
class ModelEvaluationArtifact:...
class ModelPusherArtifact:...
