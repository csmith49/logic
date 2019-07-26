from .variable import isVariable

class Substitution:
    def __init__(self, bindings=None):
        if bindings:
            self._dict = bindings
        else:
            self._dict = {}

    # union-find style target update on access
    def walk(self, key):
        if isVariable(key) and key in self._dict.keys():
            return self.walk(self._dict[key])
        else:
            return key
    def __getitem__(self, key):
        return self.walk(key)

    # treat as a static instance - simply construct a new instance
    def extend(self, key, value):
        maps = dict(self._dict)
        maps[key] = value
        return Substitution(maps)

    def isBound(self, key):
        return key in self._dict.keys()

    def __str__(self):
        return str(self._dict)