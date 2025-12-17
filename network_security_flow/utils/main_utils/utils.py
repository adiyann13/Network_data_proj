from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging
import yaml
import os
import numpy as np
import pickle
import dill
import sys



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
