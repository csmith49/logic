from logic.core import *

a_and_b = conj(
    fresh(lambda x: eq(x, 7)),
    fresh(lambda y: disj(
        eq(y, 5),
        eq(y, 6)
    ))
)

for result in run(a_and_b):
    print(result)