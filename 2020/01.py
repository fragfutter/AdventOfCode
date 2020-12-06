#!/usr/bin/pypy3

from advent import Advent
from itertools import combinations
from functools import reduce
from operator import mul
"""
"""

class Day(Advent):
    lines = True
    conversion = int

    def s(self, l):
        for x in combinations(self.data, l):
            if sum(x) == 2020:
                return reduce(mul, x)

    def solve1(self):
        return self.s(2)

    def solve2(self):
        return self.s(3)


Day.main()
