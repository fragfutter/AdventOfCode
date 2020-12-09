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
        for i in range(l):
            for j in range(i+2, l):
                s = sum(self.data[i:j])
                if s == self.solution1:
                    return max(self.data[i:j]) + min(self.data[i:j])
                if s > self.solution1:
                    break # next i

Day.main()
