from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig




import sys 

if __name__=="__main__":
    try:
        trainingPipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingPipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)

        logging.info("Initiaite data ingeation")

        dataingestionsrtifact = data_ingestion.Initiate_Data_ingestion()
        print(dataingestionsrtifact)

        
    except Exception as e:
        raise NetworkSecurityException(e,sys)




