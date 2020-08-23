import os
from sklearn.svm import SVC
from .constant import *
from joblib import load


class SVMClassifier(object):
    def __init__(self, model=None):
        if model == None:
            self.__model = SVC()
        else:
            self.__model = self.__load_model(model)

    def __load_model(self, model_name):
        return load(open(os.path.join(MODEL_DIR, model_name),'rb'))

    def predict(self, data):
        """
        Predict input data using the model
        :return: prediction
        """
        return self.__model.predict(data)

    def train(self, X,y):
        """
        Training the model
        """
        self.__model.fit(X,y)
