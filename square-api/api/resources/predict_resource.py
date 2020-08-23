import falcon
from api.utils.preprocess import preprocess
from api.utils.constant import *
from api.utils.classifier import SVMClassifier

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.NOTSET)
log_file = "{}.log".format(__name__)
f_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

class PredictResource(object):
    # return prediction based on latest model
    def __format_answer(self, answer):
        if answer[0] == '__label__nsquare':
            return "Not Square"
        else:
            return "Square"

    def on_post(self, req, resp):
        data = req.media.get("data")
        if data is not None and len(data) > 0:
            # sort files in models dir descending order, take the first
            try:
                latest_model_file = sorted(os.listdir(MODEL_DIR), reverse=True)[0]
            except:
                logger.warning("Model is missing...")
                raise falcon.HTTPInternalServerError(
                    "500 Internal Server Error", "Model is missing. Contact author to get the latest model"
                )
            clf = SVMClassifier(latest_model_file)

            data = [preprocess(data)]

            prediction = clf.predict(data)

            prediction = self.__format_answer(prediction)
            resp.media = prediction
        else:
            logger.error("Request body did not contain the data...")
            raise falcon.HTTPBadRequest(
                "400 Bad Request", "Request body did not contain the data"
            )
