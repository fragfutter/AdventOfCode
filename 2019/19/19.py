#!/usr/bin/pypy3

import re
from queue import Queue
from advent import Advent
from advent.intcode import runit
from advent.grid import Point


"""
"""



class Day(Advent):
    matrix = True
    conversion = int
    seperator = re.compile(',')

    def prepare(self):
        super(Day, self).prepare()
        self.data = self.data[0]

    def solve1(self):
        result = 0
        for x in range(50):
            for y in range(50):
                result += runit(self.data, x, y)
        return result

    def solve2(self):
        pass


Day.main()
