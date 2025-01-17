import os 
import sys 

from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
) 

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import MOdelTrainer


from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

# in this we will gonna run the configration pipeline 


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.dataingestionconfig = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.dataingestionconfig)
            dataingestionsrtifact = data_ingestion.Initiate_Data_ingestion()
            logging.info("Data Ingestion Completed")
            return dataingestionsrtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("start Data Validation")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)                                         
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data Validation Completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Data Transformation")
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Tranformation Completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Model Trainer")
            model_trainer = MOdelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Trainer Completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact = data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact = data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact =  data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    