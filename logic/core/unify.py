from .substitution import Substitution
from .variable import isVariable

from collections import deque

# check if something is iterable
def isIterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

# and if something is unifiable
def isUnifiable(obj):
    return hasattr(obj, "_unify")
        
# we don't have a maybe monad, so we'll raise an exception if we unify two un-unifiable terms
class UnificationFailure(Exception):
    def __init__(self, l, r):
        self._left = l
        self._right = r
    def __str__(self):
        return "Cannot unify terms {} and {}".format(self._left, self._right)

# wrapper around deque gives easier access to emptiness checking
class Worklist:
    def __init__(self, *args):
        self._wl = deque(args)
        self._size = len(args)
    def push(self, *values):
        self._size += len(values)
        self._wl.extend(values)
    def pop(self):
        self._size -= 1
        return self._wl.pop()
    def isEmpty(self):
        return self._size == 0

# unify python terms (relies on obj. provided mechanism for making unification constraints)
def unify(left, right, sub):
    # to avoid recursion depth limits, we maintain a worklist of constraints
    worklist = Worklist( (left, right) )

    while not worklist.isEmpty():
        # pop from the wl and simplify
        l, r = worklist.pop()
        l, r = sub.walk(left), sub.walk(right)

        # case 1 - both the same variable
        if isVariable(l) and isVariable(r) and l == r:
            return sub
        # case 2, 3 - at least one differing variable
        elif isVariable(l):
            return sub.extend(l, r)
        elif isVariable(right):
            return sub.extend(r, l)
        # case 4 - structural equality
        elif l == r:
            return sub
        # case 5 - obj-generated constraints
        elif isUnifiable(l) and isUnifiable(r):
            lType, lConstraints = l._unify()
            rType, rConstraints = r._unify()
            # if they are of the same type, we can generate constraints
            if lType == rType:
                worklist.push(zip(lConstraints, rConstraints))
            # otherwise we have to fail
            else:
                raise UnificationFailure(left, right)
        # case 6 - iterables
        elif isIterable(l) and isIterable(r):
            worklist.push(zip(iter(l), iter(r)))
        # case 7 - fail
        else:
            raise UnificationFailure(left, right)