import pytest
from SpecialHashMap import SpecialHashMap

@pytest.fixture()
def dict1():
    dict1 = {
        "a": 1,
        "b": 2,
        "c": 3,
        'value1': 11,
        'value2': 22,
        'value3': 33,
        '1': 10,
        '2': 20,
        '3': 30,
        '1, 5': 100,
        '(5, 5)': 200,
        '(10, 5)': 300,
        '(1, 5, 3)': 400,
        '(5, 5, 4)': 500,
        '10, 5, 5': 600
    }
    return dict1

class TestSpecialHashMap:
    def test_creation(self,dict1):
        testDict = SpecialHashMap(dict1)

        for k,v in dict1.items():
            assert testDict[k] == v
