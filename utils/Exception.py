from utils.logger import logging
import sys
def error_message_detail(error):
    file_name =error.__traceback__.tb_frame.f_code.co_filename
    error_message = "error occured in python script name [{0}] line number [{1}] error message [{2}]".format(file_name,error.__traceback__.tb_lineno,str(error))

    return error_message

class CustomException(Exception):
    def __init__(self,error) -> None:
        super().__init__(error)
        self.error_message =  error_message_detail(error)
        logging.critical(self.error_message)
    def __str__(self) -> str:
        return self.error_message    