from network_security_flow.components.data_ingestion import DataIngestion
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.entity.config_entity import DataIngestionConfig
from network_security_flow.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    trainingpipeline = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(trainingpipeline)
    dataingestion = DataIngestion(dataingestionconfig)
    dataingestartifact = dataingestion.initiate_data_ingestion()
    print(dataingestartifact)
    logging.info("inititae data ingestion")