#!/usr/bin/pypy3

import re
from queue import Queue
from itertools import product
from advent import Advent
from advent.intcode import Intcode
from advent.grid import Point
from advent.turtle import Turtle, N, E, S, W
from advent.repair import compress

"""
"""

PATH = ord('#')
OPEN = ord('.')
UP = ord('^')
DOWN = ord('v')
LEFT = ord('<')
RIGHT = ord('>')
NEWLINE = 10

MAPPING = {
    UP: N,
    DOWN: S,
    LEFT: W,
    RIGHT: E,
}


class NoMacro(Exception):
    pass


class Day(Advent):
    matrix = True
    conversion = int
    seperator = re.compile(',')

    def prepare(self):
        super(Day, self).prepare()
        self.data = self.data[0]
        self.generate()
        self.find_path()
        self.dump()

    def generate(self):
        input_ = Queue()
        output = Queue()
        pc = Intcode(self.data, input_, output)
        pc.start()
        pc.join()
        grid = {}
        y = 0
        x = 0
        # top left (0, 0)
        # bottom right (10, -10)
        while not output.empty():
            c = output.get()
            if c == NEWLINE:
                y -= 1
                x = 0
            else:
                grid[Point(x, y)] = c
                if c in (UP, DOWN, LEFT, RIGHT):
                    self.start = Point(x, y)
                x += 1
        self.grid = grid

    def dump(self):
        self.maxx = max([p.x for p in self.grid])
        self.miny = min([p.y for p in self.grid])
        # dump grid
        for y in range(0, self.miny - 1, -1):
            for x in range(self.maxx + 1):
                print(chr(self.grid[Point(x, y)]), sep='', end='')
            print()

    def find_path(self):
        def is_path(position):
            return self.grid.get(Point(*position), None) == PATH

        # generate a path
        position = self.start.as_tuple()
        direction = MAPPING[self.grid[self.start]]
        turtle = Turtle(position=position, direction=direction)
        path = []
        while True:
            if is_path(turtle.ahead()):
                turtle.walk()
                path.append('W')
            elif is_path(turtle.left()):
                turtle.turn_left()
                path.append('L')
            elif is_path(turtle.right()):
                turtle.turn_right()
                path.append('R')
            else:
                break
        # compress walks to number
        result = []
        counter = 0
        for p in path:
            if p == 'W':
                counter += 1
                continue
            if counter > 0:
                result.append(counter)
                counter = 0
            result.append(p)
        if counter > 0:
            result.append(counter)
        self.path = result

    def solve1(self):
        result = 0
        # find intersections
        for k, v in self.grid.items():
            if v != PATH:
                continue
            for n in k.neighbours(diagonal=False):
                if self.grid.get(n, None) != PATH:
                    break
            else:
                # all neighbours are PATH, it's an intersection
                result += abs(k.x * k.y)
        return result

    def solve2(self):
        data = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'
        data = ','.split(data)
        main, table = compress(data)
        print(main)
        print(table)
Day.main()
