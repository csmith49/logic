from .substitution import Substitution
from .variable import Variable

from itertools import count

class State:
    def __init__(self, sub=None, vars=None):
        if vars is not None:
            self._variables = vars
        else:
            self._variables = set()

        if sub is not None:
            self.substitution = sub
        else:
            self.substitution = Substitution()

    def fresh(self):
        proposals = (Variable("?_{}".format(i)) for i in count())
        for prop in proposals:
            if prop not in self.bound():
                return prop

    def bound(self):
        return self._variables

    def __str__(self):
        return str(self.substitution)

def empty():
    return State()