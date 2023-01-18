# From the jupyter notebook it can be seen that 
# 1. Ouptput class value (Pos/Neg) is highly imbalanced so we will use Smotek library to balance it. 
# We will create values for 'Pos' class 
# 2. We will replace the missing values 
# 3. Use 'Robust Scaler' to remove the impact of outliers

from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os, sys
from sklearn.preprocessing import pipeline
import pandas as pd
from sensor import utils
import numpy as np 
from sklearn.pipeline import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN


class DataTransformation:

    def __init__(self, data_transformation_config:config_entity.DataTransformationConfig,
    data_ingestion_artifact : artifact_entity.DataIngestionAtrifact):

        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)

    @classmethod
    # USe of classmethod - Without using object of class we can call this method using class name. 
    # ideally we need to create object of a class and then using that object we used to access its methods

    def get_data_transformer_object(cls) -> pipeline:

        try:
            simple_imputer = SimpleImputer(strategy = "constant", fill_value=0)
            robust_scaler = RobustScaler()

            pipeline  = Pipeline(steps = [
                ('Imputer', simple_imputer),
                ('RobustScaler', robust_scaler)
            ])
            return pipeline
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)

    def initiate_data_transformation(self,)-> artifact_entity.DataTransformationAtrifact:
        try:
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            #selecting input feature for train and test dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis = 1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis = 1)

            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df(TARGET_COLUMN)
            target_feature_test_df = test_df(TARGET_COLUMN)

            label_encoder = LabelEncoder()
            # Convert categorical values to numeric values
            label_encoder.fit(target_feature_train_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            #transforming input feature
            input_feature_train_arr = transformation_pipeline.trasnform(input_feature_train_arr)
            input_feature_test_df = transformation_pipeline.transform(input_feature_train_arr)

            smt = SMOTETomek(sampling_strategy="minority")
            logging.info(f"Before resampling in training set Input : {input_feature_train_arr.shape} Target : {target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After resampling in training set Input : {input_feature_train_arr.shape} Target : {target_feature_train_arr.shape}")

            logging.info(f"Before resampling in testing set Input : {input_feature_test_arr.shape} Target : {target_feature_test_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_test_arr, target_feature_train_arr)
            logging.info(f"After resampling in testing set Input : {input_feature_test_arr.shape} Target : {target_feature_test_arr.shape}")

            #Target encoder
            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            #save numpy array
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_train_path, 
                                        array = train_arr)
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_test_path,
                                        array = test_arr)

            utils.save_object(file_path = self.data_transformation_config.transform_object_path, 
                            obj = transformation_pipeline)
            
            utils.save_object(file_path = self.data_transformation_config.target_encoder_path, 
                                obj = label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationAtrifact(
                transform_object_path = self.data_transformation_config.transform_object_path, 
                transformed_train_path = self.data_transformation_config.transformed_train_path, 
                trannsformed_test_path = self.data_transformation_config.transformed_test_path, 
                target_encoder_path = self.data_transformation_config.target_encoder_path
                )

            logging.info(f"Data Transformation Object {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise SensorException(error_message =e, error_detail = sys)