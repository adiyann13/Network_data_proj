from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.entity.config_entity import DataTransformationConfig
from network_security_flow.entity.artifact_entity import DataValidationAtrtifacts,DataTransformationArtifacts
import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security_flow.constants.training_pipeline import TRGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security_flow.utils.main_utils.utils import save_np_array, save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationAtrtifacts , data_transformation_config:DataTransformationConfig ):
        try:
            self.data_validation_artifact:DataValidationAtrtifacts = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetwrokExceptions(e,sys) from e 
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def imputing(cls)->Pipeline:
        try:
            knn_imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline([("imputer", knn_imputer)])
            return processor
        except Exception as e:
            raise NetwrokExceptions(e,sys)

    
    def initiate_data_transformation(self)->DataTransformationArtifacts:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            indep_ft_train_df = train_df.drop(columns = [TRGET_COLUMN], axis=1)
            dep_ft_train_df = train_df[TRGET_COLUMN]
            dep_ft_train_df = dep_ft_train_df.replace(-1,0)

            indep_ft_test_df = test_df.drop(columns = [TRGET_COLUMN], axis=1)
            dep_ft_test_df = test_df[TRGET_COLUMN]
            dep_ft_test_df = dep_ft_test_df.replace(-1,0)

            preprocessor_imp = self.imputing()
            preprocessor_objects= preprocessor_imp.fit(indep_ft_train_df)
            preprocessor_train_df = preprocessor_objects.transform(indep_ft_train_df)
            preprocessor_test_df = preprocessor_objects.transform(indep_ft_test_df)

            train_arr = np.c_[preprocessor_train_df,np.array(dep_ft_train_df)]
            test_arr = np.c_[preprocessor_test_df,np.array(dep_ft_test_df)]

            save_np_array(self.data_transformation_config.transformed_train_file_path,  array=train_arr,)
            save_np_array(self.data_transformation_config.transformed_test_file_path , array=test_arr,)
            save_object(self.data_transformation_config.tranformed_object_file_path,preprocessor_objects,)

            save_object('final_model/preprocessor.pkl', preprocessor_objects)

            data_transformation_artifacts = DataTransformationArtifacts (
                transformed_object_file_path = self.data_transformation_config.tranformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path

            )

            return data_transformation_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)