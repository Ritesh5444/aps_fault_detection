from sensor.predictor import ModelResolver
from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException


class ModelEvaluation:

    def __init(self,
    model_eval_config : config_entity.ModelEvaluationConfig,
     data_ingestion_artifact : artifact_entity.DataIngestionAtrifact,
     data_transformation_artifact :artifact_entity.DataTransformationAtrifact,
     model_trainer_artifact: artifact_entity.ModelTrainerArtifact)
     try:
        pass
    except Exception as e:
        raise SensorException(error_message= e, error_detail = sys)

    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:

            #if saved model folder has model then we will compare
            #which model is best trained or the model from saved folder

            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted, improved_accuracy = None)
                return model_eval_artifact
            
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)
        
     