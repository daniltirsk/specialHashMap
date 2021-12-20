import re

class SpecialHashMap(dict):
    @property
    def iloc(self):
        return _iLocIndexer(self)

    @property
    def ploc(self):
        return _pLocIndexer(self)

class _iLocError(Exception):
    pass

class _iLocIndexer():
    def __init__(self,hmap):
        self.hmap = hmap

    def __getitem__(self, key):
        if isinstance(key,slice):
            return self._getitem_vector(key)
        if isinstance(key,int):
            return self._getitem_scalar(key)
        else:
            raise _iLocError("Indices must be of type integer")

    def _getitem_scalar(self,key):
        self._check_key(key)
        return self.hmap[sorted(self.hmap.keys())[key]]

    def _getitem_vector(self,key):
        self._check_slice(key)
        return [self.hmap[k] for k in sorted(self.hmap.keys())[key]]

    def _check_key(self,key):
        if not isinstance(key, int):
            raise _iLocError("Indices must be of type integer")
        if key >= len(self.hmap):
            raise _iLocError("Index out of bounds")

        return True

    def _check_slice(self,slice):
        slice_keys = [slice.start,slice.stop,slice.step]
        for key in slice_keys:
            if key == None:
                continue
            if not isinstance(key, int):
                raise _iLocError("Indices must be of type integer")
        return True

        

class _pLocError(Exception):
    pass

class _pLocIndexer():
    def __init__(self,hmap):
        self.hmap = hmap

    def __getitem__(self, key):
        result = []

        condition_vals, condition_operators = self._extract_conditions(key)

        keys = self.hmap.keys()

        for k in keys:
            k_vals = self._extract_key_values(k)
            if self._evaluate_conditions(k_vals,condition_vals,condition_operators):
                result.append(self.hmap[k])
        return result

    def _extract_conditions(self,key):
        p = re.compile('((?:<>)|[<>=]=?)\s*((?:\d+\.?\d*)|(?:\.\d+))')
        conditions = p.findall(key)
        condition_vals = [float(c[1]) for c in conditions]
        condition_operators = [c[0] for c in conditions]

        return condition_vals,condition_operators

    def _extract_key_values(self,key):
        pk = re.compile('(?<!\w)((?:\d+\.?\d*)|(?:\.\d+))')
        k_vals = [float(k) for k in pk.findall((key))]
        return k_vals

    def _evaluate_conditions(self,key_vals,values,conditions):
        if len(key_vals) != len(conditions):
            return False

        for k,val,cond in zip(key_vals,values,conditions):
            if cond == ">":
                if not k > val:
                    return False
            elif cond == "<":
                if not k < val:
                    return False
            elif cond == "==":
                if not k == val:
                    return False
            elif cond == "<>":
                if not k != val:
                    return False
            elif cond == ">=":
                if not k >= val:
                    return False
            elif cond == "<=":
                if not k <= val:
                    return False
            else:
                raise _pLocError('Invalid condition')
        return True