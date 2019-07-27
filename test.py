from logic.core import *

# TEST 1
test_1 = query(lambda q: freshN(2, lambda x, y: conj(eq(q, (1, x)), eq(q, (y, 2)))))
assert(next(test_1) == (1, 2))

print("All OK")