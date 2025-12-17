from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
import yaml
import os
import numpy as np
import pickle
import dill
import sys

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml(file_path:str)-> dict:
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetwrokExceptions(e,sys)


def write_yaml_file(file_path:str , content:object , replace:bool =False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path , "w") as file:
            yaml.dump(content , file)
    except Exception as e:
        raise NetwrokExceptions(e,sys)
    
def save_np_array(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path , 'wb') as fl:
            np.save(fl, array)
    except Exception as e:
        raise NetwrokExceptions(e,sys)

def save_object(file_path:str, obj:object):
    try:
        dir_path =os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok=True)
        with open(file_path , 'wb') as fl2:
            pickle.dump(obj , fl2)
    except Exception as e:
        raise NetwrokExceptions(e,sys)

def load_object(file_path:str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception("file does not exist")
        with open(file_path, "rb") as fl:
            return pickle.load(fl)
    except Exception as e:
        raise NetwrokExceptions(e,sys)


def load_np_arrray(file_path:str)->np.array:
    try:
        with open(file_path ,"rb") as npfl:
            return np.load(npfl)
    except Exception as e:
        raise NetwrokExceptions(e,sys)

def evaluate_models(X_train,Y_train,X_test,Y_test,models,params):
    try:
        report:dict ={}
        fitted_models = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model_name = list(models.keys())[i]
            param = params[model_name]

            gs = GridSearchCV(model,param,cv=3)
            gs.fit(X_train,Y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)

            fitted_models[model_name] = model

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(Y_train, y_train_pred)
            test_model_score = r2_score(Y_test,y_test_pred)

            report[model_name] = test_model_score

        return report, fitted_models
    except Exception as e:
        raise NetwrokExceptions(e,sys)