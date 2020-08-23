import os
import ast
from typing import List

import numpy as np
from scipy.interpolate import interp1d
from api.utils.constant import *

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.NOTSET)
log_file = "{}.log".format(__name__)
f_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

TRUNCATE_LIMIT = 30
TIME_NORM = 100
X_NORM = 10
Y_NORM = 10
PAD_MAX = TRUNCATE_LIMIT
STEP = TRUNCATE_LIMIT / 2


def truncate(data: list) -> list:
    """
    Truncate data to a certain length, allowing svm classifier to fit (train)
    """
    result = []
    for time, x, y in data:
        if len(result) == TRUNCATE_LIMIT:
            logger.info("Truncation limit reached. Truncating...")
            break
        else:
            result.append([time,x,y])
    return result

def pad(data: list) -> list:
    """
    Pad short data to be long enough for training, allowing svm classifier to fit (train)
    """
    if len(data) > PAD_MAX:
        logger.info("Padding unnecessary. Skipping...")
        return data

    padding = [[0,0,0]] * (PAD_MAX - len(data))

    data.extend(padding)

    return data

def normalize(data: list) -> list:
    """
    Normalize the data without changing the interpolation
    """
    time_init, x_init, y_init = data[0]
    normalized_data = [[time/ TIME_NORM, (x - x_init) / X_NORM, (y - y_init) / Y_NORM]for time, x, y in data]
    return normalized_data

def interpolate(data: list) -> list:
    """
    Interpolate the data to retain its timeliness
    """
    time_data, x_data, y_data = [],[],[]
    for time, x, y in data:
        time_data.append(time)
        x_data.append(x)
        y_data.append(y)


    fx = interp1d(time_data, x_data)
    fy = interp1d(time_data, y_data)

    # + 0.001 to include the max time data
    points = np.arange(min(time_data), max(time_data)+0.001, STEP)
    xnew = fx(points)
    ynew = fy(points)

    return [[points[i],xnew[i],ynew[i]]for i in range(len(points))]


def skinny(data: list) -> list:
    """
    Remove time data, and reshape from 2D to 1D data for training
    """
    a, b = [], []
    for time, x, y in data:
        a.append(x)
        b.append(y)
    return list(a) + list(b)

def preprocess(data: list) -> list:
    """
    Preprocessing pipeline
    """
    data = interpolate(data)
    data = normalize(data)
    data = truncate(data)
    data = pad(data)
    data = skinny(data)
    return data

def json2text(data: list) -> list:
    """
    Convert json data to text data for saving
    """
    result = []
    for ks, vs in data.items():
        if ks == "square":
            for v in vs:
                v = legitimize(v)
                if is_valid(v):
                    result.append('__label__square {}\n'.format(v))
                else:
                    continue

        if ks == "nsquare":
            for v in vs:
                v = legitimize(v)
                if is_valid(v):
                    result.append('__label__nsquare {}\n'.format(v))
                else:
                    continue

    return result

def x_y_split(file_path: str):
    """
    Split x and y for training
    """
    X = []
    y = []
    with open(file_path, 'r') as f:
        data = f.read().splitlines()
        for d in data:
            d = d.split(' ')
            X.append(ast.literal_eval(''.join(d[1:])))
            y.append(d[0])

    return X, y

def legitimize(data: list) -> list:
    """
    Avoid interpolation error (division by 0)
    """
    result = []
    prev = -1
    for time, x, y in data:
        if time == prev:
            logger.warning("Duplicated timestamp found. Removing...")
            continue
        else:
            prev = time
            result.append([time, x, y])
    return result

def is_valid(data: list) -> list:
    """
    Check if data input is valid (length must be minimal = 2)
    """
    if len(data) == 0:
        logger.warning("Empty data found. Removing...")
        return False
    if len(data) == 1:
        print(data)
        logger.warning("Insufficient data for prediction. Removing...")
    else:
        return True
