from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
import os, sys
import pandas as pd
from typing import Optional
from sensor import utils
import numpy as np


class DataValidation:

    def __init__(self,data_validation_config: config_entity.DataValidationConfig, 
    data_ingestion_artifact : artifact_entity.DataIngestionAtrifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")

            self.data_validation_config = data_validation_config
            self.validation_error = dict()
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SensorException(error_message =e, error_detail = sys)


    #Dropping columns above a threshold value
    def drop_missing_values_columns(self,df:pd.DataFrame, report_key_name: str)->Optional[pd.DataFrame]:
        """
        This function will drop columns which contains missing value more than a specified threshold

        df : Accepts a dataframe
        threshold : Percentage criteria to drop a column

        =========================================================================
        returns pandas Dataframe if atleast single column is available
        
        """
        #Option[] has been used if no columns are satisfying the criteria of 0.2
        #  threshold and we don't get any record
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #Selecting column names which contains null values
            logging.info(f"selecting column name which contain null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names),axis = 1, inplace = True)
            
            # return none if no columns left
            if len(df.columns) == 0:
                return None
            return df
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)

    #Checking for number of columns
    def is_required_columns_exist(self,base_df:pd.DataFrame, current_df:pd.DataFrame,report_key_name:str)-> bool:
        try:
            
            base_columns = base_df.columns
            current_columns = current_df.base_columns

            missing_columns = []
            for base_columns in base_columns:
                if base_columns not in current_columns:
                    logging.info(f"column : [{base} is not availabe]")
                    missing_columns.append(base_column)

            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True
        except Exception as e:
            raise SensorException(e, sys)

    def data_drift(self, base_df : pd.DataFrame, current_df:pd.DataFrame,report_key_name: str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns =current_df.columns

            for base_column in base_columns:
                base_data,current_data = base.df[base_column], current_df[base_column]
                #Null hypothesis is that both column data form same distribution

                logging.info(f"Hypothesis {base_column}: {base_data.dtype}", {current_data.dtype})
                same_distirbution  = ks_2samp(base_data,current_data)

            if same_distirbution.pvalue > 0.05:
                #We are accepting NULL hypothesis
                drift_report[base_column] = {
                    "pvalues": float(same_distirbution.pvalue),
                    "same_distribution": True
                }
            else:
                drift_report[base_column] = {
                    "pvalues": float(same_distirbution.pvalue),
                    "same_distribution": False
                }
                #Different distribution

            self.validation_error[report_key_name] = drift_report
                
        except Exception as e:
            raise SensorException(e, sys)


    
    def initiate_data_validation(self,) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN}, inplace = True)
            logging.info(f"Replace na value in base df")
            #Base df has na as NULL
            logging.info(f"Drop null value colmuns from base df")
            base_df = self.drop_missing_values_columns(df = base_df,report_key_name= "missing_values_within_base_dataset")

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Drop null column values from train df")
            train_df = self.drop_missing_values_columns(df = train_df,report_key_name = "missing_values_within_train_dataset")
            logging.info(f"Drop null column values from test df")
            test_df = self.drop_missing_values_columns(df = test_df,report_key_name = "missing_values_within_test_dataset")

            exclude_columns = ["class"]
            base_df = utils.convert_columns_float(df = base_df, exclude_columns = exclude_columns)
            train_df = utils.convert_columns_float(df = train_df, exclude_columns = exclude_columns)
            test_df = utils.convert_columns_float(df = test_df, exclude_columns = exclude_columns)

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exist(base_df= base_df, current_df = train_df,report_key_name = "missing_values_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exist(base_df= base_df, current_df = test_df,report_key_name = "missing_values_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df = base_df, current_df =train_df,report_key_name = "data_drift_within_train_dataset")
            
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df = base_df, current_df = test_df,report_key_name = "data_drift_within_test_dataset")

            #Write the report
            logging.info("Write report in YAML file")
            utils.write_yaml_file(file_path = self.data_validation_config.report_file_path,
             data = self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path = self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact : {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)