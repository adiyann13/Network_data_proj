import os
import sys
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
from network_security_flow.entity.artifact_entity import DataTransformationArtifacts,ModelTrainerArtifcats
from network_security_flow.entity.config_entity import ModelTrainerConfig

from network_security_flow.utils.main_utils.utils import save_np_array, save_object, load_object
from network_security_flow.utils.main_utils.utils import load_np_arrray
from network_security_flow.utils.ml_utils.metrics.classifiaction_metrics import get_classification_score
from network_security_flow.utils.ml_utils.models.estimator import NetworkModel
from network_security_flow.utils.main_utils.utils import evaluate_models

from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import mlflow
import dagshub

dagshub.init(repo_owner='adiyannmd', repo_name='Network_data_proj', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig , data_transform_artifacts:DataTransformationArtifacts):
        try:
            self.model_trainer_config =  model_trainer_config
            self.data_transform_artifacts =data_transform_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    
    def track_mlflow(self,best_model,clasificationmetric):
        with mlflow.start_run():
            f1_score = clasificationmetric.f1_score
            precison_score = clasificationmetric.precision
            recall_score = clasificationmetric.recall

            mlflow.log_metric("fl_score", f1_score)
            mlflow.log_metric("precision", precison_score)
            mlflow.log_metric("recall", recall_score)

            mlflow.sklearn.log_model(best_model, "model")

    
    def train_model(self,x_train,y_train, x_test, y_test):
        try:
            models ={
                "Random_Forest":RandomForestClassifier(verbose=1),
                "DecisionTree": DecisionTreeClassifier(),
                "AdaBoost":AdaBoostClassifier(),
                "GradientBoosting":GradientBoostingClassifier(verbose=1),
                "Logistic_Regression":LogisticRegression(verbose=1)
            }

            params={
                "DecisionTree":{
                    'criterion':['gini','entropy'],
                    'max_depth':[2,5,7],

                },
                "Random_Forest":{
                    'n_estimators':[80,100,120],

                },
                "AdaBoost":{
                    'learning_rate':[0.001,0.01,0.1,0.5],
                    'n_estimators':[60,80,100]

                },
                "GradientBoosting":{
                    'loss':['log_loss','exponential'],
                    'subsample':[0.5,0.7,0.9,1.0],
                    'n_estimators':[100,130,150]
                },
                "Logistic_Regression":{
                }
            }
            model_report, fitted_models = evaluate_models(X_train=x_train ,Y_train = y_train , X_test = x_test, Y_test = y_test, models = models,params=params)
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = fitted_models[best_model_name]
            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train , y_pred = y_train_pred)
            
            ##ml flow
            self.track_mlflow(best_model , classification_train_metric)

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

            self.track_mlflow(best_model , classification_test_metric)

            preprocessor = load_object(file_path=self.data_transform_artifacts.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_mod = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path , network_mod)

            model_trainer_artifact = ModelTrainerArtifcats(trained_model_file_path=self.model_trainer_config.trained_model_file_path , 
                                  train_metric_artifact=classification_train_metric ,test_metric_artifact=classification_test_metric)

            return model_trainer_artifact
        except Exception as e:
            raise NetwrokExceptions(e,sys)
        
        
    def initiate_model_training(self)->ModelTrainerArtifcats:
        try:
            train_file_path = self.data_transform_artifacts.transformed_train_file_path
            test_file_path = self.data_transform_artifacts.transformed_test_file_path

            train_arr = load_np_arrray(train_file_path)
            test_arr = load_np_arrray(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1],
            )

            model_trainer_artifacts = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifacts
        except Exception as e:
            raise NetwrokExceptions(e,sys)


