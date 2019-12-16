#!/usr/bin/pypy3

import re
from queue import Queue
from collections import defaultdict
from advent import Advent
from advent.intcode import Intcode
from advent.grid import Point
from advent.astar import Node, Astar

"""
"""

BLOCKED = 0
OK = 1
OXYGEN = 2

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

UNKNOWN = None
WALL = '#'
EMPTY = '.'
TARGET = 'O'
STEP = '+'


class Robot(object):
    def __init__(self, code):
        self.input_ = Queue()
        self.output = Queue()
        self.pc = Intcode(code, self.input_, self.output)
        self.pc.daemon = True
        self.pc.start()
        self.grid = defaultdict(lambda: UNKNOWN)
        self.grid = dict()
        self.pos = Point(0, 0)
        self.grid[self.pos] = EMPTY
        self.target = None

    def step(self, direction):
        self.pc.waiting_for_input.clear()
        self.input_.put(direction)
        self.pc.waiting_for_input.wait()
        result = self.output.get()
        # calculate new position
        if direction == NORTH:
            npos = self.pos.north()
        elif direction == SOUTH:
            npos = self.pos.south()
        elif direction == EAST:
            npos = self.pos.east()
        elif direction == WEST:
            npos = self.pos.west()
        else:
            Exception('unknown direction')
        if result == BLOCKED:
            self.grid[npos] = WALL
            return result
        # store information
        if result == OK:
            self.grid[npos] = EMPTY
        elif result == OXYGEN:
            self.target = npos
            self.grid[npos] = TARGET
        else:
            Exception('unknown return code')
        # update position
        self.pos = npos
        return result

    def dump_grid(self):
        mx = 0
        my = 0
        Mx = 0
        My = 0
        xs = [p.x for p in self.grid]
        ys = [p.y for p in self.grid]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                if Point(x, y) == self.pos:
                    print('D', sep ='', end = '')
                else:
                    print(self.grid.get(Point(x, y), ' '), sep='', end='')
            print()


class GridNode(Node):
    def __init__(self, x, y, grid):
        super(GridNode, self).__init__(x, y)
        self.grid = grid

    @property
    def neighbours(self):
        pos = Point(self.x, self.y)
        for n in pos.neighbours(diagonal=False):
            if self.grid.get(n, None) in (EMPTY, TARGET):
                yield GridNode(n.x, n.y, self.grid)


class Day(Advent):
    matrix = True
    conversion = int
    seperator = re.compile(',')

    def prepare(self):
        super(Day, self).prepare()
        self.data = self.data[0]

    def solve1(self):
        robot = Robot(self.data)
        trace = []
        while True:
            if robot.pos.north() not in robot.grid:
                if robot.step(NORTH) != BLOCKED:
                    trace.append(SOUTH)
            elif robot.pos.east() not in robot.grid:
                if robot.step(EAST) != BLOCKED:
                    trace.append(WEST)
            elif robot.pos.south() not in robot.grid:
                if robot.step(SOUTH) != BLOCKED:
                    trace.append(NORTH)
            elif robot.pos.west() not in robot.grid:
                if robot.step(WEST) != BLOCKED:
                    trace.append(EAST)
            else:
                # backtrack
                try:
                    robot.step(trace.pop())
                except IndexError:
                    break
        # maze complete, solve it
        start = GridNode(0, 0, robot.grid)
        end = GridNode(robot.target.x, robot.target.y, robot.grid)
        astar = Astar(start, end)
        solution = astar.solve()
        steps = 0
        while solution.parent:
            steps += 1
            solution = solution.parent
        robot.dump_grid()
        self.robot = robot
        return steps

    def solve2(self):
        minutes = 0
        has_update = True
        while has_update:
            has_update = False
            current = [pos for pos, value in self.robot.grid.items() if value == TARGET]
            for c in current:
                for n in c.neighbours(diagonal=False):
                    if self.robot.grid[n] == EMPTY:
                        self.robot.grid[n] = TARGET
                        has_update = True
            minutes += 1
        return minutes - 1  # last round no update


Day.main()
