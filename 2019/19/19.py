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
        self.create_basemap()

    def create_basemap(self):
        # there is a gap beweeen (0, 0) and the first affected field
        # iterate the area to (10, 10) to get starting values
        grid = {}
        for x in range(10):
            for y in range(10):
                grid[Point(x, y)] = runit(self.data, x, y)
        self.grid = grid

    def create_map(self, limit):
        # expand grid to cover area up to limit
        limit = limit - 1
        grid = self.grid
        work = [p for p, v in grid.items() if v]
        while work:
            p = work.pop(0)
            grid[p] = runit(self.data, p.x, p.y)
            if not grid[p]:
                continue
            for n in p.neighbours(diagonal=True):
                if n in work:
                    continue
                if n.x < 0 or n.y < 0:
                    continue
                if n.x > limit or n.y > limit:
                    continue
                if n in grid:
                    continue
                work.append(n)
        self.grid = grid
        result = sum(grid.values())
        return result

    def solve1(self):
        self.create_map(50)
        return sum(self.grid.values())

    def sample_grid(self):
        with open('sample.txt') as fh:
            data = fh.read()
        result = {}
        for y, row in enumerate(data.split('\n')):
            for x, c in enumerate(row):
                result[Point(x, y)] = int(c != '.')
        return result

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
        p = Point(x, y)
        if p in self.grid:
            return self.grid[p]
        v = runit(self.data, x, y)
        self.grid[p] = v
        return v

    def solve2(self):
        size = 100 - 1
        # start in the last known row, our grid is to small anyway
        y = max([p.y for p, v in self.grid.items() if v])
        x = min([p.x for p, v in self.grid.items() if v and p.y == y])
        lx = x
        while True:
            if self.get(x + size, y):
                if self.get(x, y+size):
                    break  # found it
                else:
                    # but we can go right
                    x += 1
                    continue
            # nothing to the right, new row
            y += 1
            # find lower left corner
            while not self.get(lx, y):
                lx += 1
            x = lx
        return x * 10000 + y


Day.main()
