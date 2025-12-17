from network_security_flow.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import sys
import os
from network_security_flow.exceptions.exception import NetwrokExceptions
from network_security_flow.logging.logger import logging


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model =model
        except Exception as e:
            raise NetwrokExceptions(e,sys)
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transfrom(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetwrokExceptions(e,sys)