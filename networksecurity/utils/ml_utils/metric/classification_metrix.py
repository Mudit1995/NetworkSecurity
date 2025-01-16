from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exceptin import NetworkSecurityException

from sklearn.metrics import f1_score,precision_score,recall_score
import sys

# from here we will have 3 things that we will return in the form of the  ClassificationMetricArtifact which is f1 score , precision score and recall score 


def get_classification_score(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        # these paramter are their ro configure the accuracy of the model 
        model_f1_score = f1_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        classification_metric = ClassificationMetricArtifact(f1_score=model_f1_score,precision_score=model_precision_score,recall_score=model_recall_score)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)

 
