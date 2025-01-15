from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation





import sys 

if __name__=="__main__":
    try:
        trainingPipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingPipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)

        logging.info("Initiaite data ingeation")

        dataingestionsrtifact = data_ingestion.Initiate_Data_ingestion()
        logging.info("data ingestion completed")
        print(dataingestionsrtifact)


        data_validation_config = DataValidationConfig(trainingPipelineconfig)
        data_validation = DataValidation(dataingestionsrtifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("data Validation Completed")






        
    except Exception as e:
        raise NetworkSecurityException(e,sys)




