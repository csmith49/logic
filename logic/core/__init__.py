from .goal import Goal, conj, disj, cond
from .stream import Stream
from .unify import unify, UnificationFailure
from .substitution import Substitution
from .state import State, empty

# recreating part of the interface from muKanren
def take(stream, n=None):
    if n is not None:
        return list(islice(stream, n))
    else:
        return list(stream)

def run(goal):
    stream = goal(empty())
    return take(stream)
def run_n(n, goal):
    stream = goal(empty())
    return take(stream, n=n)

def eq(l, r):
    def goal(state):
        try:
            sub = unify(l, r, state.substitution)
            state = State(sub=sub, vars=state.bound())
            return Stream.unit(state)
        except UnificationFailure:
            return Stream.mzero()
    return Goal(goal)

def fresh(closure):
    def goal(state):
        v = state.fresh()
        varSet = set([v] + list(state.bound()))
        state = State(sub=state.substitution, vars=varSet)
        return closure(v)(state)
    return Goal(goal)