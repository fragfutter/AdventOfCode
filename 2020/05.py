#!/usr/bin/pypy3

from advent import Advent
from functools import reduce
from operator import mul

"""
"""

def seatid(row, col):
    return row * 8 + col


class Day(Advent):
    lines = True
    translation = ''.maketrans('FBLR', '0101')
    fb = [2**x for x in range(7-1, -1, -1)]
    lr = [2**x for x in range(3-1, -1, -1)]

    def conversion(self, line):
        line = line.translate(self.translation)
        result = list(map(int, line))
        return result

    def solve1(self):
        self.seats = {}
        for line in self.data:
            row = sum([a*b for (a, b) in zip(self.fb, line[:7])])
            col = sum([a*b for (a, b) in zip(self.lr, line[7:])])
            self.seats[(row, col)] = seatid(row, col)
        return max(self.seats.values())

    def solve2(self):
        ids = self.seats.values()
        for row in range(128):
            for col in range(8):
                id_ = seatid(row, col)
                if id_ in ids:
                    continue  # taken
                # check neighbours, they must be taken
                if id_ - 1 not in ids:
                    continue
                if id_ + 1 not in ids:
                    continue
                return id_


Day.main()
