#!/usr/bin/pypy3

from advent import Advent
import advent.grid

"""
"""
SEAT = 'L'
FLOOR = '.'
PERSON = '#'


class Point(advent.grid.Point):
    def los_neighbours(self, grid):
        """line of sight neighbours"""
        directions = ('north', 'south', 'east', 'west',
                      'northwest', 'northeast', 'southwest', 'southeast')
        for d in directions:
            p = getattr(self, d)()
            while p in grid and grid[p] == FLOOR:
                p = getattr(p, d)()
            if p in grid:
                yield p


def life1(grid):
    result = {}
    change = False
    for point, value in grid.items():
        if value == FLOOR:
            result[point] = FLOOR
            continue
        # count persons
        count = sum([grid.get(n, None) == PERSON for n in point.neighbours()])
        if value == SEAT:
            if count > 0:
                # at least one neighbour, stay empty
                result[point] = SEAT
            else:
                result[point] = PERSON
                change = True
        elif value == PERSON:
            if count < 4:
                result[point] = PERSON
            else:
                # four or more neighbours, vacate
                result[point] = SEAT
                change = True
        else:
            raise Exception('what?')
    return result, change


def life2(grid):
    result = {}
    change = False
    for point, value in grid.items():
        if value == FLOOR:
            result[point] = FLOOR
            continue
        # count persons
        count = sum([grid[n] == PERSON for n in point.los_neighbours(grid)])
        if value == SEAT:
            if count > 0:
                # at least one neighbour, stay empty
                result[point] = SEAT
            else:
                result[point] = PERSON
                change = True
        elif value == PERSON:
            if count < 5:
                result[point] = PERSON
            else:
                # four or more neighbours, vacate
                result[point] = SEAT
                change = True
        else:
            raise Exception('what?')
    return result, change


class Day(Advent):
    def prepare(self):
        result = {}
        for row, line in enumerate(self.data.split('\n')):
            for col, seat in enumerate(line.strip()):
                result[Point(col, row)] = seat
        self.data = result

    def solve1(self):
        count = 0
        grid, change = life1(self.data)
        while change:
            count += 1
            grid, change = life1(grid)
        print(count)  # iterations
        # count persons
        return sum([v == PERSON for v in grid.values()])

    def solve2(self):
        count = 0
        grid, change = life2(self.data)
        while change:
            count += 1
            grid, change = life2(grid)
        print(count)  # iterations
        # count persons
        return sum([v == PERSON for v in grid.values()])


Day.main()
