from network_security_flow.components.data_ingestion import DataIngestion
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.entity.config_entity import DataIngestionConfig
from network_security_flow.entity.config_entity import TrainingPipelineConfig
from network_security_flow.components.data_validation import DataValidation
from network_security_flow.entity.config_entity import DataValidationConfig
from network_security_flow.components.data_transformation import DataTransformation
from network_security_flow.entity.config_entity import DataTransformationConfig
if __name__ == '__main__':
    trainingpipeline = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingpipeline)
    dataingestion = DataIngestion(dataingestionconfig)
    dataingestartifact = dataingestion.initiate_data_ingestion()
    print(dataingestartifact)
    logging.info("inititae data ingestion")


    logging.info("completed data ingestion")

    datavalidationconfig = DataValidationConfig(trainingpipeline)
    datavalidation = DataValidation(dataingestartifact, datavalidationconfig)
    logging.info("initiating dsata validation")
    data_valid_artifact = datavalidation .initiate_data_validation()
    print(data_valid_artifact)
    logging.info("dv completed")


    logging.info("transformation odf data started")

    datatransformationconfig = DataTransformationConfig(trainingpipeline)
    datatrasnformation = DataTransformation(data_valid_artifact, datatransformationconfig)
    data_trans_artifacts = datatrasnformation.initiate_data_transformation()
    print(data_trans_artifacts)
    logging.info("transformation done")



