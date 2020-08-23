import os
import falcon
from joblib import dump
import json
from api.utils.constant import *
from api.utils.classifier import SVMClassifier
from api.utils.preprocess import *

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.NOTSET)
log_file = "{}.log".format(__name__)
f_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

class RetrainResource(object):
    def __init__(self):
        self.__model = SVMClassifier()

    # perform retraining
    def on_post(self, req, resp):
        """
        Retrain the model using the latest data
        """
        # sort file descending, take the first
        latest_data_file = sorted(os.listdir(DATA_DIR), reverse=True)[0]
        try:
            latest_model_file = sorted(os.listdir(MODEL_DIR), reverse=True)[0]
        except:
            latest_model_file = '-1'

        X, y = x_y_split(os.path.join(DATA_DIR, latest_data_file))

        X = [preprocess(x) for x in X]

        # clf.fit, can create classifier object here
        self.__model.train(X, y)

        # create new file with filename +1
        filename = str(int(latest_model_file) + 1)
        dump(self.__model, open(os.path.join(MODEL_DIR, filename),'wb'))
        logger.info("Retraining completed")

    def on_post_add_data(self, req, resp):
        """
        Add training data for retraining
        """
        req_data = req.media
        if req_data is not None:
            latest_data_file = sorted(os.listdir(DATA_DIR), reverse=True)[0]
            new_data_file = str(int(latest_data_file) + 1)

            req_text_data = json2text(req_data)
            with open(os.path.join(DATA_DIR, latest_data_file),'r') as old_file:
                originial_text_data = old_file.readlines()

            req_text_data.extend(originial_text_data)

            with open(os.path.join(DATA_DIR, new_data_file),'w') as new_file:
                for data in req_text_data:
                    new_file.write(data)

            logger.info("Retraining data successfully uploaded")
        else:
            raise falcon.HTTPBadRequest(
                "400 Bad Request", "Request body did not contain greylist key"
            )
