from .substitution import Substitution
from .variable import Variable
from .unify import unify

from itertools import count
from copy import deepcopy

class State:
    '''State objects maintain all constraints necessary to satisfy goals'''

    __slots__ = ("substitution", "variables", "_extensions")
    def __init__(self):
        self.variables = set()
        self.substitution = Substitution()
        self._extensions = {}

    def freshVariable(self):
        proposals = (Variable("?.{}".format(i)) for i in count())
        for prop in proposals:
            if prop not in self.variables:
                return prop
    
    def __str__(self):
        return f"{self.substitution} - {self.variables}"

    def addFreshVariable(self):
        var = self.freshVariable()
        result = self.clone()
        result.variables.add(var)
        return var, result

    def clone(self):
        return deepcopy(self)

    def unify(self, left, right):
        result = self.clone()
        result.substitution = unify(left, right, self.substitution)
        return result
        
def empty():
    return State()