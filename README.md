# Logic

Implementation of a relational logic language in Python.

## Design Philosophy

This is intended to be a small library that is easy to include in any projects where solving a logic problem is a core step. Efficiency is *not* the concern, usability is, but we do want searches to terminate whenever possible.

To develop, we proceed in two steps:

1. Implement a core of muKanren (see references)
2. Extend with helper functions to ease integration into a Python workflow

## References

[The OG reference](http://webyrd.net/scheme-2013/papers/HemannMuKanren2013.pdf)
[Interesting use cases](https://www.cs.tufts.edu/~nr/cs257/archive/william-byrd/kanren-solving-pearl.pdf)
