from logic.core import *

x_and_y = freshN(2, lambda x, y:
    conj(
        eq(x, 7),
        disj(
            eq(y, 5),
            eq(y, 6)
        ),
        eq(x, y)
    )
)

or_test = query(lambda x:
    disj(
        eq(x, 1),
        eq(x, 2),
        eq(x, 3)
    )
)

for result in run(x_and_y):
    print(result)