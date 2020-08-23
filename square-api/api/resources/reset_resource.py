import os
from api.utils.constant import *

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.NOTSET)
log_file = "{}.log".format(__name__)
f_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

class ResetResource(object):
    def on_post(self, req, resp):
        """
        Remove all data except for base data
        """
        self.remove_data()
        self.remove_models()

    def on_post_data(self, req, resp):
        """
        Remove files from data dir except for 0 (base data)
        """
        self.remove_data()


    def on_post_model(self, req, resp):
        """
        Remove files from model dir except for 0 (base model)
        """
        self.remove_models()
        logger.info("Resetting retraining data...")


    @staticmethod
    def remove_data():

        files = os.listdir(DATA_DIR)
        for file in files:
            if file != '0':
                os.remove(os.path.join(DATA_DIR,file))

    @staticmethod
    def remove_models():

        files = os.listdir(MODEL_DIR)
        for file in files:
            if file != '0':
                os.remove(os.path.join(MODEL_DIR,file))

        logger.info("Resetting retrained models...")
