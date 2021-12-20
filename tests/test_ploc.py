import pytest
from SpecialHashMap import SpecialHashMap, _pLocError

@pytest.fixture()
def dict1():
    dict1 = {
        'value1': 1,
        'value2': 2,
        'value3': 3,
        '1': 10,
        '2': 20,
        '3': 30,
        "(1, 5)": 100,
        "(5, 5)": 200,
        "(10, 5)": 300,
        "(1, 5, 3)": 400,
        "(5, 5, 4)": 500,
        "(10, 5, 5)": 600,
    }
    return dict1

@pytest.fixture()
def conditions():
    conditions = [">=1","<3",">0, >0",">= 10 aa   >0","<5, >=5, >=3"]
    return conditions

@pytest.fixture()
def extracted_conditions():
    condition_vals = [[1],[3],[0,0],[10,0],[5,5,3]]
    condition_operators = [[">="],["<"],[">",">"],[">=",">"],["<",">=",">="]]
    return condition_vals, condition_operators



class TestILoc:
    def test_creation(self, dict1):
        testDict = SpecialHashMap(dict1)
        assert testDict.ploc.hmap == testDict

    def test_get_item(self, dict1,conditions):
        testDict = SpecialHashMap(dict1)

        assert testDict.ploc[">=1"] == [10,20,30]  # >>> {1=10, 2=20, 3=30}
        assert testDict.ploc["<3"] == [10,20] # >>> {1=10, 2=20}
        assert testDict.ploc[">0, >0"] == [100,200,300] # >>> {(1, 5)=100, (5, 5)=200, (10, 5)=300}
        assert testDict.ploc[">= 10 aa   >0"] == [300] # >>> {(10, 5)=300}
        assert testDict.ploc["<5, >=5, >=3"] == [400] # >>> {(1, 5, 3)=400}

    def test_extract_key_values(self, dict1):
        testDict = SpecialHashMap(dict1).ploc

        assert testDict._extract_key_values('value1') == []
        assert testDict._extract_key_values('1') == [1]
        assert testDict._extract_key_values('(10, 5, 5)') == [10,5,5]
        assert testDict._extract_key_values('(10;5;5)') == [10,5,5]

    def test_extract_conditions(self,dict1 , conditions, extracted_conditions):
        testDict = SpecialHashMap(dict1).ploc
        expected_vals = extracted_conditions[0]
        expected_operators = extracted_conditions[1]
        for cond,e_vals,e_ops in zip(conditions,expected_vals,expected_operators):
            c_vals,c_operators = testDict._extract_conditions(cond)
            assert c_vals == e_vals
            assert c_operators == e_ops

    def test_evaluate_conditions(self,dict1,extracted_conditions):
        testDict = SpecialHashMap(dict1).ploc

        condition_vals, condition_operators = extracted_conditions

        expected_matches = [['1', '2', '3'],['1', '2'],['(1, 5)', '(5, 5)', '(10, 5)'], ['(10, 5)'], ['(1, 5, 3)']]

        for cond_val,cond_op,e_match in zip(condition_vals, condition_operators, expected_matches):
            for k in testDict.hmap.keys():
                k_vals = testDict._extract_key_values(k)
                if k in e_match:
                    assert testDict._evaluate_conditions(k_vals, cond_val, cond_op)
                else:
                    assert not testDict._evaluate_conditions(k_vals, cond_val, cond_op)

        with pytest.raises(_pLocError):
            testDict._evaluate_conditions([1,2,4], [1,2,3], [">>","<<","!="])