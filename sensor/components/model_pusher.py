from sensor.predictor import ModelResolver
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationAtrifact, ModelTrainerArtifact,ModelPusherArtifact
import os,sys
from sensor.utils import load_object,save_object
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.artifact_entity import ModelPusherArtifact


class ModelPusher:

    def __init__(self, model_pusher_config: ModelPusherConfig,data_transformation_artifact : DataTransformationAtrifact,
    model_trainer_artifact : ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry= self.model_pusher_config.saved_model_dir)

        except Exception as e:
            raise SensorException(e,sys)


    def initiate_model_pusher(self,) ->ModelPusherArtifact:
        try:
            #load object
            logging.info(f"Loading transformer model and target encoder")
            transformer = load_object(file_path = self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path = self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path = self.data_transformation_artifact.target_encoder_path)

            #Model pusher dir
            save_object(file_path = self.model_pusher_config.pusher_transformer_path, obj = transformer)
            save_object(file_path = self.model_pusher_config.pusher_model_dir, obj = model)
            save_object(file_path= self.model_pusher_config.pusher_target_encoder_path, obj = target_encoder)

            #saved model dir
            
            save_object(file_path = self.model_resolver.get_latest_transformer_path(), obj = transformer)
            save_object(file_path = self.model_resolver.get_latest_save_model_path(), obj = model)
            save_object(file_path= self.model_resolver.get_latest_save_target_encoder_path(), obj = target_encoder)

            save_object(file_path = tranfomer_path, obj = transformer)
            save_object(file_path = model_path, obj = model)
            save_object(file_path = target_encoder_path, obj = target_encoder)

            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir = self.model_pusher_config.pusher_model_dir,
             saved_model_dir = self.model_pusher_config.saved_model_dir)
            loggig.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact



            pass
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)

