import sys
import os

class NetwrokExceptions(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"error occured in script name {self.file_name} line number {self.lineno} and message is : {str(self.error_message)}"
    