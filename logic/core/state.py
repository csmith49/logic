from .substitution import Substitution
from .variable import Variable

from itertools import count

class State:
    def __init__(self, substitution, variables=None):
        self.variables = set() if variables is None else variables
        self.substitution = substitution

    def bound(self):
        return self.variables

    def freshVariable(self):
        proposals = (Variable("?.{}".format(i)) for i in count())
        for prop in proposals:
            if prop not in self.bound():
                return prop
    
    def __str__(self):
        return str(self.substitution)

    def extend(self):
        var = self.freshVariable()
        variables = set(list(self.variables) + [var])
        return var, State(self.substitution, variables=variables)

def empty():
    emptySub = Substitution()
    return State(emptySub)