from .goal import Goal, conj, disj, cond
from .stream import Stream
from .unify import unify, UnificationFailure
from .reify import reify
from .substitution import Substitution
from .state import State, empty
from .variable import Variable, isVariable

# recreating part of the interface from muKanren
def run(goal, numResults=None):
    stream = goal(empty())
    if numResults:
        stream = islice(stream, numResults)
    return list(stream)

def query(closure):
    x, state = empty().addFreshVariable()
    for result in closure(x)(state):
        yield reify(x, result)

# the simplest goal - we just try to unify
def eq(l, r):
    def goal(state):
        try:
            return Stream.unit(state.unify(l, r))
        except UnificationFailure:
            return Stream.mzero()
    return Goal(goal)

# even simpler, really - never give anything
def fail():
    def goal(state):
        return Stream.mzero()
    return Goal(goal)

# for ease of use with variables
def var(v):
    return Variable(v)

# fresh represents our usage of HOAS to avoid dealing with variable naming schemes
def fresh(closure):
    def goal(state):
        x, state = state.addFreshVariable()
        return closure(x)(state)
    return Goal(goal)

def freshN(n, closure):
    def goal(state):
        variables = []
        for _ in range(n):
            x, state = state.addFreshVariable()
            variables.append(x)
        return closure(*variables)(state)
    return Goal(goal)