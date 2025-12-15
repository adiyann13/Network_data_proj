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
