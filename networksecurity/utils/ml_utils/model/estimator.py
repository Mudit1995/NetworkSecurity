import os 
import sys 

from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME


# What's happening here:

# The NetworkModel class is a wrapper that combines:

# The preprocessor (your Pipeline with KNNImputer)
# The trained model (best_model)


# When you save this to a pickle file:

# Both the preprocessor and model are saved together
# This ensures that future predictions will use the exact same preprocessing steps


# The key benefit is that when you load this model later:

# You can make predictions on raw data
# The NetworkModel will automatically:

# Preprocess the data using the saved preprocessor
# Make predictions using the saved model

class NetowrkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    


    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
