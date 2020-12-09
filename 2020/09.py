#!/usr/bin/pypy3

from advent import Advent
from itertools import combinations
"""
"""

class Day(Advent):
    lines = True
    conversion = int
    preamble = 25

    def solve1(self):
        preamble = self.preamble
        for i in range(len(self.data) - preamble):
            b = self.data[i:i+preamble]
            v = self.data[i+preamble]
            if v not in [a + b for a, b in combinations(b, 2)]:
                self.solution1 = v  # remember it for part2
                return v

    def solve2(self):
        l = len(self.data)
        # do it with a moving window
        i = 0  # start of range
        j = 0  # end of range
        s = 0  # current sum
        while s != self.solution1:
            if s < self.solution1:
                s += self.data[j]
                j += 1
            else:
                s -= self.data[i]
                i += 1
        return min(self.data[i:j]) + max(self.data[i:j])

Day.main()
