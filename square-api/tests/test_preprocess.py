from api.utils.preprocess import *

def test_truncacte():
    assert truncate([[1,0,0]] * 31) == [[1,0,0]] * 30
    assert truncate([[1,0,0]] * 29) == [[1,0,0]] * 29

def test_pad():
    sample_1 = [[1,1,1]]
    sample_1.extend([[0,0,0]] * 29)
    assert pad([[1,1,1]]) == sample_1
    assert pad([[1,1,1]] * 51) == [[1,1,1]] * 51

def test_normalize():
    assert normalize([[0,0,0],[100,100,100],[200,200,200]]) == [[0.0,0.0,0.0],[1.0,10.0,10.0],[2.0,20.0,20.0]]

def test_interpolate():
    assert interpolate([[0,0,0],[30,18,24],[45,20,24]])== [[0,0,0],[15,9,12],[30,18,24],[45,20,24]]

def test_skinny():
    assert skinny([[1,2,3],[4,5,6],[7,8,9]]) == [2,5,8,3,6,9]
