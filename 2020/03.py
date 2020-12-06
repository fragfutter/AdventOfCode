#!/usr/bin/pypy3

from advent import Advent
from functools import reduce
from operator import mul

"""
"""

class Day(Advent):
    lines = True

    def conversion(self, line):
        result = [tree == '#' for tree in line]
        return result

    def count_trees(self, right=3, down=1):
        col = 0
        result = 0
        for row in self.data[::down]:
            try:
                tree = row[col]
            except IndexError:
                col -= len(row)
                tree = row[col]
            if tree:
                result += 1
            col += right
        return result

    def solve1(self):
        return self.count_trees(right=3, down=1)

    def solve2(self):
        result = [
            self.count_trees(1),
            self.count_trees(3),
            self.count_trees(5),
            self.count_trees(7),
            self.count_trees(1, 2)
        ]
        return reduce(mul, result)


Day.main()
