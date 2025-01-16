import os 
import sys

from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact

from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.main_utils.utils import evaluate_models

from networksecurity.utils.ml_utils.metric.classification_metrix import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetowrkModel 


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ( RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier) 

class MOdelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            "Logistic Regression": LogisticRegression(verbose=1),
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
            # "KNeighborsClassifier": KNeighborsClassifier(),
        }

        # perform hypermatric tuning 
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }      
        }

        model_report:dict=evaluate_models(x_train,y_train,x_test,y_test,models,params)

        # get the besat model score from dict 
        best_model_score = max(sorted(model_report.values()))
        
        # to get the  best model name 
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

        best_model = models[best_model_name]

        y_train_pred=best_model.predict(x_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        # track in the MLFLOW 
        


        # we will gonna have the pkl file which will gonna save the best model which we have and the processor also which is KNNimputer  
        # 1. load the precprocessor 
        # 2.make a path for the pickle file object director and sabe it a
        # 3. call the netwotk model for the object creation which is a wrapper c;lass havong both preprocessor and model 
        #. and save the object 


        # This is wer are actually just trying to make the director before hand 
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path) 

        Netowrk_Model = NetowrkModel(preprocessor=preprocessor,model = best_model)

        save_object(self.model_trainer_config.trained_model_file_path, Netowrk_Model)

        ## create a MODEL trainr artifact 
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, train_metric_artifact = classification_train_metric, test_metric_artifact = classification_test_metric)

        logging.info("Model trainer artifact ")

        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            # loading the data array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],    # All columns except last for features
                train_arr[:, -1],     # Only last column for target
                test_arr[:, :-1],     # All columns except last for features
                test_arr[:, -1]       # Only last column for target
            )
            
            modeltrainerartifact = self.train_model(x_train, y_train,x_test, y_test)
            return modeltrainerartifact


        except Exception as e:
            raise NetworkSecurityException(e, sys)
