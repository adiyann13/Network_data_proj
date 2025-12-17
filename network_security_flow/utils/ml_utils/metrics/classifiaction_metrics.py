from network_security_flow.entity.artifact_entity import ClassificationMetricsArtifacts
from network_security_flow.exceptions.exception import NetwrokExceptions
from sklearn.metrics import f1_score,precision_score,recall_score
import sys



def get_classification_score(y_true,y_pred)->ClassificationMetricsArtifacts:
    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_precision = precision_score(y_true,y_pred)
        model_recall = recall_score(y_true, y_pred)

        classification_metrics = ClassificationMetricsArtifacts(f1_score = model_f1_score , precision=model_precision , recall=model_recall)
        return classification_metrics
    except Exception as e:
        raise NetwrokExceptions(e,sys)