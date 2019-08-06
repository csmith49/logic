from logic.core import *
from logic.relation import Fact, observe

# TEST 1 - general usage
test_1 = get(lambda q: freshN(2, lambda x, y: eq(q, (1, x)) & eq(q, (y, 2))))
assert(next(test_1) == (1, 2))

# TEST 2 - unification across objects
class Foo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

test_2 = get(lambda q: eq(Foo(q, 2), Foo(1, 2)))
assert(next(test_2) == 1)

# TEST 3 - failing query
test_3 = freshN(2, lambda x, y: conj(eq(x, 7), (eq(y, 5) | eq(y, 6)), eq(x, y)))
assert(run(test_3) == [])

# TEST 4 - relation stuff
tbl = observe(
    Fact("father", "Steve", "Alice"),
    Fact("mother", "Erica", "Alice")
)

def parent(tbl, child):
    return get(lambda x: Fact("father", x, child) | Fact("mother", x, child), state=tbl)

assert("Steve" in parent(tbl, "Alice"))
assert("Erica" in parent(tbl, "Alice"))

print("All OK")