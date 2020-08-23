from api.utils.constant import *

def test_BASE_DIR():
    assert '/'.join(BASE_DIR.split('/')[-2:]) == 'square-app/api'

def test_DATA_DIR():
    assert '/'.join(DATA_DIR.split('/')[-3:]) == 'square-app/api/data'

def test_MODEL_DIR():
    assert '/'.join(MODEL_DIR.split('/')[-3:]) == 'square-app/api/models'
