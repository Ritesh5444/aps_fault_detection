from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
import os, sys
import pandas as pd
from typing import Optio

class DataValidation:

    def __init__(self,data_validation_config: config_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")

            self.data_validation_config = data_validation_config
            self.validation_error = dict()
        except Exception as e:
            raise SensorException(error_message =e, error_detail = sys)


    #Dropping columns above a threshold value
    def drop_missing_values_columns(self,)->Option[pd.Dataframe]:
        """
        This function will drop columns which contains missing value more than a specified threshold

        df : Accepts a dataframe
        threshold : Percentage criteria to drop a column

        =========================================================================
        returns pandas Dataframe if atleast single column is available
        
        """
        #Option[] has been used if no columns are satisfying the criteria of 0.3 threshold and we don't get any record
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #Selecting column names which contains null values
            drop_column_names = null_report[null_report>threshold].index

            self.validation_error["dropped_columns"] = drop_column_names    
            df.drop(list(drop_column_names),axis = 1, inplace = True)
            
            # return none if no columns left
            if len(df.columns) == 0:
                return None
            return df
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)

    #Checking for number of columns
    def is_required_columns_exist(self,base_df:pd.DataFrame, current_df:pd.DataFrame)-> bool:
        try:
            
            base_columns = base_df.columns
            current_columns = current_df.base_columns

            missing_columns = []
            for base_columns in base_columns:
                if base_columns not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns) > 0:
                self.validation_error["Missing columns"] = missing_columns
                return False
            return True
        except Exception as e:
            raise SensorException(e, sys)

    def data_drift(self, base_df : pd.DataFrame, current_df:pd.DataFrame):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns =current_df.columns

            for base_column in base_columns:
                base_data,current_data = base.df[base_column], current_df[base_column]
                #Null hypothesis is that both column data form same distribution
                same_distirbution  = ks_2samp(base_data,current_data)

            if same_distirbution.pvalue > 0.05:
                #We are accepting NULL hypothesis
                drift_report[base_column]- {
                    "pvalues": same_distirbution.pvalue,
                    "same_distribution": True
                }
            else:
                drift_report[base_column]- {
                    "pvalues": same_distirbution.pvalue,
                    "same_distribution": False
                }
                
        except Exception as e:
            raise SensorException(e, sys)


    
    def initiate_data_validation(self,) -> artifact_entity.DataValidationArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)