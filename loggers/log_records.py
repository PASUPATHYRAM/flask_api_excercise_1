import os
import logging
from logging.handlers import RotatingFileHandler

class Logcreator:

    def __init__(self):
        self.log=logging.getLogger(__name__)
        self.log.setLevel(logging.ERROR)
        self.format=logging.Formatter('%(asctime)s - %(message)s')

        if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__name__),'log.log'))):
            file=open('log.log','a')
            file.close()
        self.file_han=RotatingFileHandler('log.log',backupCount=5,maxBytes=1000)
        self.file_han.setFormatter(self.format)
        self.log.addHandler(self.file_han)

    def message(self,message):
        self.log.error(message)

