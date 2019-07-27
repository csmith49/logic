from logic.core import *

# TEST 1 - general usage
test_1 = query(lambda q: freshN(2, lambda x, y: conj(eq(q, (1, x)), eq(q, (y, 2)))))
assert(next(test_1) == (1, 2))

# TEST 2 - unification across objects
class Foo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

test_2 = query(lambda q: eq(Foo(q, 2), Foo(1, 2)))
assert(next(test_2) == 1)

# TEST 3 - failing query
test_3 = freshN(2, lambda x, y: conj(eq(x, 7), (eq(y, 5) or eq(y, 6)), eq(x, y)))
assert(run(test_3) == [])

print("All OK")