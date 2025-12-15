from network_security_flow.entity.artifact_entity import DataIngestionArtifacts, DataValidationAtrtifacts
from network_security_flow.entity.config_entity import DataValidationConfig
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys
from  network_security_flow.constants.training_pipeline import DATA_SCHEMA_FILE_PATH
from network_security_flow.utils.main_utils.utils import read_yaml, write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact : DataIngestionArtifacts , data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml(DATA_SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    @staticmethod
    def read_data(file_path:str) ->pd.DataFrame:
        return pd.read_csv(file_path)
    
    def validating_data(self,dataframe:pd.DataFrame) -> bool:
        try:
            no_of_cols = len(self.schema_config)
            logging.info(f'reuired cols is {no_of_cols}')
            df_cols  = len(dataframe.columns)
            logging.info(f'dataframe is cols {df_cols}')
            if len(dataframe.columns) == no_of_cols:
                return True 
            else:
                return False
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def numerical_data_check(self,dataframe:pd.DataFrame) ->bool:
        try:
            for cols in dataframe.columns:
                if dataframe[cols].dtype == 'int64' or  dataframe[cols].dtype == 'float64':
                    return True
                else:
                    return False
        except Exception as e:
            raise NetwrokExceptions(e,sys)

    def detect_datset_drift(self, base_df, current_df , threshold =0.05) -> bool:
        try:
            status =True
            report ={}
            for cols in base_df.columns:
                d1= base_df[cols]
                d2 = current_df[cols]
                sample_dist = ks_2samp(d1,d2)
                if threshold <= sample_dist.pvalue:
                    is_found = False
                else:
                    is_found =True
                    status=False
                report.update({cols:{"p_value": float(sample_dist.pvalue),
                                       "drift_status" : is_found}})
            
            drift_report_file_path = self.data_validation_config.data_drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path ,exist_ok=True)
            write_yaml_file(file_path= drift_report_file_path ,content=report)
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    

    def initiate_data_validation(self) -> DataValidationAtrtifacts:
        try:
            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_pth = self.data_ingestion_artifact.testing_file_path

            training_dataframe = DataValidation.read_data(train_file_path)
            testing_dataframe = DataValidation.read_data(test_file_pth)

            train_status = self.validating_data(training_dataframe)
            if train_status == True:
                 error_mssg = f"the trainin data  columns are same its validated data"
            
            test_status = self.validating_data(testing_dataframe)
            if test_status == True:
                error_mssg = f'the testing data column are same its validated'
            
            train_num_check = self.numerical_data_check(training_dataframe)
            if train_num_check == True:
                num_check = f'the training  df has numericla data '
            
            test_num_check = self.numerical_data_check(testing_dataframe)
            if test_num_check == True:
                num_check =f'the testing  df has numerical data in it '
            drift_status = self.detect_datset_drift(base_df=training_dataframe , current_df=testing_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path  ,exist_ok=True)

            training_dataframe.to_csv(self.data_validation_config.valid_train_file_path ,index=False ,header=True)
            data_validation_artifact = DataValidationAtrtifacts(
                validation_status = drift_status,
                valid_train_file_path = self.data_ingestion_artifact.training_file_path,
                valid_test_file_path = self.data_ingestion_artifact.testing_file_path,
                invalid_train_path =  None,
                invalid_test_path = None,
                drift_report_file_path = self.data_validation_config.data_drift_report_file_path,

            )
            return data_validation_artifact
        except Exception as e:
            raise NetwrokExceptions(e,sys)
        



