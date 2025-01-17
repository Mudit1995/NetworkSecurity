import os 
import sys 
from networksecurity.exception.exceptin import NetworkSecurityException

import pandas as pd 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline 
from sklearn.impute import KNNImputer

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (DataTransformationArtifact,DataValidationArtifact)

from networksecurity.entity.config_entity import DataTransformationConfig
# from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

import numpy as np


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @classmethod
    def get_data_tranformer_object(cls) -> Pipeline:
        logging.info("Enter get _data_tranfomer_object method of tranfomration class")
        try:
            # this star indicates that it is goven in the key value imputer 
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("initiailise the KNN iimputer" )
            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def initiate_data_transformation(self)-> DataTransformationArtifact:
        logging.info("Enter inot the instaitae the data Trnasformation")
        try:
            logging.info("Start data Tranformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)


            # Reove the target Column and training dataframe 
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)


            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            input_feature_train_arr = imputer.fit_transform(input_feature_train_df)
            input_feature_test_arr = imputer.transform(input_feature_test_df)

            # implement KNN imputer
            preprcessor = self.get_data_tranformer_object()
            preprcessor_object = preprcessor.fit(input_feature_train_df)
            transformwe_input_train_feature = preprcessor_object.transform(input_feature_train_df)
            transformwe_input_test_feature = preprcessor_object.transform(input_feature_test_df)
            # fir actually When you call fit(), KNNImputer:
            # Records the locations of missing values
            # Learns the structure of relationships between datapoints
            # But doesn't actually fill in any values yet


            # The actual imputation happens during transform(), where for each missing value it:

            # Finds the k-nearest neighbors based on the other features
            # Uses those neighbors' values to fill in the missing value
            # By default, it uses the mean of the neighbor values, but you can specify other methods

            # we are combnining above array into the numpy 
            train_arr = np.c_[transformwe_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformwe_input_test_feature,np.array(target_feature_test_df)]

            # save numpy array data 
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)

            # save the preprocessor object calling the pickle file 
            save_object(self.data_transformation_config.transformed_object_file_path,preprcessor_object)
            save_object("final_model/preprocessing.pkl",preprcessor_object)

            # preparing the artifacts 

            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifacts
             

        except Exception as e:
            raise NetworkSecurityException(e,sys)