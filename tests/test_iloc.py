import pytest
from SpecialHashMap import SpecialHashMap, _iLocError


@pytest.fixture()
def dict1():
    dict1 = {
        'value1': 1,
        'value2': 2,
        'value3': 3,
        '1': 10,
        '2': 20,
        '3': 30,
        '1, 5': 100,
        '5, 5': 200,
        '10, 5': 300,
    }
    return dict1

@pytest.fixture()
def validKeys():
    keys = [1,2,3,4,5,0,-1,-5]
    return keys

@pytest.fixture()
def invalidKeys():
    keys = ['908',7567,89.0,(89),[89],{9:6}]
    return keys

@pytest.fixture()
def validSlices():
    keys = [slice(0,1,2),slice(5,2,-1),slice(666,6,6)]
    return keys

@pytest.fixture()
def invalidSlices():
    keys = [slice('ad','ds',3),slice([43],4,-1),slice({'fs':45})]
    return keys

class TestILoc:
    def test_creation(self, dict1):
        testDict = SpecialHashMap(dict1)
        assert testDict.iloc.hmap == testDict

    def test_check_key(self,dict1,validKeys,invalidKeys):
        testDict = SpecialHashMap(dict1).iloc

        for k in validKeys:
            assert testDict._check_key(k)

        for k in invalidKeys:
            with pytest.raises(_iLocError):
                testDict._check_key(k)

    def test_check_slice(self,dict1,validSlices,invalidSlices):
        testDict = SpecialHashMap(dict1).iloc

        for k in validSlices:
            assert testDict._check_slice(k)

        for k in invalidSlices:
            with pytest.raises(_iLocError):
                testDict._check_slice(k)

    def test_get_single(self,dict1):
        testDict = SpecialHashMap(dict1)

        assert testDict.iloc[0] == 10
        assert testDict.iloc[2] == 300
        assert testDict.iloc[5] == 200
        assert testDict.iloc[8] == 3

    def test_get_vector(self,dict1):
        testDict = SpecialHashMap(dict1)

        assert testDict.iloc[0:2] == [10, 100]
        assert testDict.iloc[5:2:-1] == [200, 30, 20]
        assert testDict.iloc[10:10:10] == []