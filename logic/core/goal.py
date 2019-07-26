from functools import reduce
from operator import and_, or_

# we operate under the assumption that f has type f : state -> iter(state)
class Goal:
    def __init__(self, f):
        self._closure = f

    def __and__(self, other):
        def closure(state):
            return self(state) >> other
        return Goal(closure)
    
    def __or__(self, other):
        def closure(state):
            return self(state) + other(state)
        return Goal(closure)

    def __call__(self, state):
        return self._closure(state)
    
def conj(*goals):
    base, *rest = goals
    return reduce(and_, rest, base)

def disj(*goals):
    base, *rest = goals
    return reduce(or_, rest, base)

def cond(*clauses):
    return disj(conj(*clause) for clause in clauses)