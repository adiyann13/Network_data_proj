import os
import sys
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.components.data_ingestion import DataIngestion
from network_security_flow.components.data_validation import DataValidation
from network_security_flow.components.data_transformation import DataTransformation
from network_security_flow.components.model_trainer import ModelTrainer

from network_security_flow.entity.config_entity import DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig,TrainingPipelineConfig
from network_security_flow.entity.artifact_entity import DataIngestionArtifacts,DataTransformationArtifacts,DataValidationAtrtifacts,ModelTrainerArtifcats
from network_security_flow.cloud.s3_syncer import S3Sync
from network_security_flow.constants.training_pipeline import TRAINING_BUCKET_NAME
from network_security_flow.entity.config_entity import TrainingPipelineConfig
from network_security_flow.constants.training_pipeline import SAVED_MODEL_DIR

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("start data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def start_data_validation(self,data_ingestion_artifacts:DataIngestionArtifacts):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifacts , data_validation_config=self.data_validation_config)
            data_validation_artifacts = data_validation.initiate_data_validation()
            return data_validation_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def start_data_transformation(self,data_validation_artifacts:DataValidationAtrtifacts):
        try:
            self.data_transformation_conifg = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifacts, data_transformation_config=self.data_transformation_conifg)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)
        
    def start_model_trainer(self,data_transform_artifacts:DataTransformationArtifacts):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_training = ModelTrainer(model_trainer_config=self.model_trainer_config , data_transform_artifacts=data_transform_artifacts)
            model_trainer_artifacts = model_training.initiate_model_training()
            return model_trainer_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)

    def sync_artifact_to_s3(self):
        try:
            aws_bucket_url = f's3://{TRAINING_BUCKET_NAME}/Artifacts/{self.training_pipeline_config.timestamp}'
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,s3_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def sync_model_to_s3(self):
        try:
            aws_bucket_url = f's3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}'
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir,s3_bucket_url = aws_bucket_url)
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_trnsformation_artifacts = self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts = self.start_model_trainer(data_transform_artifacts=data_trnsformation_artifacts)

            self.sync_artifact_to_s3()
            self.sync_model_to_s3()
            return model_trainer_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)

