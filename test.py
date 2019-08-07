from logic.core import *
from logic.relation import fact, observe

# TEST 1 - general usage
test_1 = query(lambda q: bind(lambda x, y: eq(q, (1, x)) & eq(q, (y, 2))))
print(f"Testing {test_1}: expecting q = (1, 2)...")
assert(next(run(test_1)) == (1, 2))
print("OK\n")

# TEST 2 - unification across objects
class Foo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"Foo({self.x}, {self.y})"

test_2 = query(lambda q: eq(Foo(q, 2), Foo(1, 2)))
print(f"Testing {test_2}: expecting q = 1...")
assert(next(run(test_2)) == 1)
print("OK\n")

# TEST 3 - failing query
test_3 = bind(lambda x, y: conj(eq(x, 7), (eq(y, 5) | eq(y, 6)), eq(x, y)))
print(f"Testing {test_3}: expecting no solution...")
assert(list(run(test_3)) == [])
print("OK\n")

# TEST 4 - relation stuff
tbl = observe(
    fact("father", "Steve", "Alice"),
    fact("mother", "Erica", "Alice")
)

def parent(child):
    return query(lambda x: fact("father", x, child) | fact("mother", x, child))
test_4 = parent("Alice")
print(f"Testing {test_4}: expecting 'Steve' and 'Erica'...")
results = run(test_4, state=tbl)
assert("Steve" in results)
assert("Erica" in results)
print("OK\n")

print("All OK")