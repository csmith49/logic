from .substitution import Substitution
from .variable import isVariable

from collections import deque
from collections.abc import Iterable

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
    def push(self, value):
        self._size += 1
        self._wl.append(value)
    def extend(self, iter):
        iter = list(iter)
        self._size += len(iter)
        self._wl.extend(iter)
    def pop(self):
        self._size -= 1
        return self._wl.pop()
    def isEmpty(self):
        return self._size == 0

# unify python terms (relies on obj. provided mechanism for making unification constraints)
# TODO - fix to be more efficient
def unify(left, right, sub):
    # to avoid recursion depth limits, we maintain a worklist of constraints
    worklist = Worklist( (left, right) )

    while not worklist.isEmpty():
        # pop from the wl and simplify
        left, right = worklist.pop()
        left, right = sub.find(left), sub.find(right)

        # case 1 - both the same variable
        if isVariable(left) and isVariable(right) and left == right:
            pass
        # case 2, 3 - at least one differing variable
        elif isVariable(left):
            sub = sub.extend(left, right)
        elif isVariable(right):
            sub = sub.extend(right, left)
        # case 4 - structural equality
        elif left == right:
            pass
        # case 5 - object
        elif hasattr(left, "__dict__") and hasattr(right, "__dict__") and type(left) == type(right):
            worklist.push( (left.__dict__, right.__dict__) )
        # case 6 - dictionary
        elif isinstance(left, dict) and isinstance(right, dict):
            leftKeys, rightKeys = set(left.keys()), set(right.keys())
            if len(leftKeys ^ rightKeys) == 0:
                ccs = [(left[key], right[key]) for key in leftKeys]
                worklist.extend(ccs)
            else:
                raise UnificationFailure(left, right)
        # case 7 - tuple
        elif isinstance(left, tuple) and isinstance(right, tuple):
            if len(left) == len(right):
                worklist.extend(zip(left, right))
            else:
                raise UnificationFailure(left, right)
        # case 8 - list
        elif isinstance(left, list) and isinstance(right, list):
            if len(left) == len(right):
                worklist.extend(zip(left, right))
            else:
                raise UnificationFailure(left, right)
        # case 9 - iterable
        elif isinstance(left, Iterable) and isinstance(right, Iterable):
            leftList, rightList = list(left), list(right)
            if len(leftList) == len(rightList):
                return worklist.extend(zip(leftList, rightList))
            else:
                raise UnificationFailure(left, right)
        # case 10 - failure
        else:
            raise UnificationFailure(left, right)
    # if all constraints are resolved, we can return
    return sub