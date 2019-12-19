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
        self.grid = {}

    def create_map(self, limit):
        # note that the starting area has rows without affected fields
        # so we need to trace a few rows completely up to limit
        y = 0
        x = 0
        while not self.get(x, y) and x < limit:
            x += 1
        while y < limit:
            if x == limit:
                x = 0
            while not self.get(x, y) and x < limit:
                x += 1  # find lower left in case we did not have it
            lx = x  # remember for the next row
            while self.get(x, y) and x < limit:
                x += 1  # hit all affected fields
            y += 1
            x = lx

    def solve1(self):
        self.create_map(50)
        return sum(self.grid.values())

    def dump(self, grid, hl=None):
        xlimit = max([p.x for p in grid])
        ylimit = max([p.y for p in grid])
        for y in range(ylimit):
            for x in range(xlimit):
                p = Point(x, y)
                v = grid[p]
                if hl and p == hl:
                    if v:
                        c = '0'
                    else:
                        c = '.'
                else:
                    if v:
                        c = '#'
                    else:
                        c= ' '
                print(c, sep='', end='')
            print()

    def get(self, x, y):
        # get grid value and cache it
        if x < 0 or y < 0:
            return 0
        p = Point(x, y)
        if p in self.grid:
            return self.grid[p]
        v = runit(self.data, x, y)
        self.grid[p] = v
        return v

    def solve2(self):
        size = 100 - 1
        x = 0
        y = size  # we check above right, so minimum y is size
        # find the first affected field
        while not self.get(x, y):
            x += 1
        while True:
            # check diagonal above right
            if self.get(x + size, y - size):
                # got it, get top left corner
                result = x, y - size
                break
            # new row, left corner
            y += 1
            while not self.get(x, y):
                x += 1
        return result[0] * 10000 + result[1]


Day.main()
