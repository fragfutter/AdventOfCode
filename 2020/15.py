#!/usr/bin/pypy3

from advent import Advent

"""
"""

class Day(Advent):
    def prepare(self):
        self.data = list(map(int, self.data.strip().split(',')))

    def work(self, end):
        turn = 0
        last = None
        spoken = {}
        # initialize
        for n in self.data:
            turn += 1
            spoken[n] = (turn, turn)
            last = n
        # iterate
        while turn < end:
            turn += 1
            a, b = spoken[last]
            n = b - a
            try:
                spoken[n] = (spoken[n][1], turn)
            except KeyError:
                # never spoken before
                spoken[n] = (turn, turn)
            last = n
        return last

    def solve1(self):
        return self.work(2020)

    def solve2(self):
        return self.work(30000000)


Day.main()
