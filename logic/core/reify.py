from .variable import isVariable

from collections.abc import Iterable

# unlike unification, this shouldn't get called often, so recursion is probably fine here
def reify(term, s):
    sub = s.substitution
    # if term is a var, just look it up in s
    if isVariable(term) and sub.isBound(term):
        return reify(sub[term], s)
    # if we can represent term by a dict, recurse on the dict
    elif hasattr(term, "__dict__"):
        d = reify(term.__dict__, s)
        if d == term.__dict__:
            return term
        else:
            obj = object.__new__(type(term))
            obj.__dict__.update(d)
            return obj
    # if term _is_ a dict, recurse on values
    elif isinstance(term, dict):
        return {k : reify(v, s) for k, v in term.items()}
    # if term is a tuple, map reifying over everything
    elif isinstance(term, tuple):
        return tuple(reify(iter(term), s))
    # if term is a list, map reifying over everything
    elif isinstance(term, list):
        return list(reify(iter(term), s))
    # if term is an iterable, make new one by lazily reifying
    elif isinstance(term, Iterable):
        def generator():
            for item in iter(term):
                yield reify(item, s)
        return generator()
    # otherwise, just pass the term back as-is
    else:
        return term
    