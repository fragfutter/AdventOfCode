#!/usr/bin/pypy3

from advent import Advent

"""
"""

def neighbours(coordinates):
    def recursion(dimension):
        if not dimension:
            # final
            yield ()
            return
        for outer in recursion(dimension - 1):
            start = coordinates[dimension - 1] - 1
            stop = coordinates[dimension - 1] + 1
            for inner in range(start, stop + 1):
                yield outer + (inner, )

    for c in recursion(len(coordinates)):
        if c != coordinates:
            yield c


class Grid(object):
    def __init__(self, points=[]):
        self.data = set()  # use a set, faster lookup (120 seconds -> 2 seconds)
        for point in points:
            self.activate(point)

    def activate(self, point):
        self.data.add(point)  # no need to check no duplicates in sets

    def deactivate(self, point):
        try:
            self.data.remove(point)
        except KeyError:
            pass

    def iterate(self, offset=1):
        def recursion(dimension):
            if not dimension:
                # final
                yield ()
                return
            for outer in recursion(dimension - 1):
                values = [x[dimension - 1] for x in self.data]
                start = min(values) - offset
                stop = max(values) + offset
                for inner in range(start, stop + 1):
                    yield outer + (inner, )

        # next(iter(self.data)) => first element of set
        for coordinates in recursion(len(next(iter(self.data)))):
            yield coordinates

    def count_neighbours(self, point):
        result = 0
        for n in neighbours(point):
            if n in self.data:
                result += 1
        return result


class Day(Advent):
    matrix = True
    # conversion = lambda x: x=='#'

    def prepare(self):
        result = []
        for y, line in enumerate(self.data.split('\n')):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    result.append((x, y))
        self.data = result

    def solve_(self, dimensions):
        extension = (0, ) * (dimensions - 2)
        result = Grid()
        for coordinates in self.data:
            result.activate(coordinates + extension)
        for i in range(6):
            new = Grid()
            for point in result.iterate():
                count = result.count_neighbours(point)
                if point in result.data:
                    # if an activate point has 2 or 3 neighbours
                    # it stays active
                    if count in (2, 3):
                        new.activate(point)
                    # otherwise it becomes inactive
                else:
                    # if an inactivate point has 3 neighbours
                    # it becomes active
                    if count == 3:
                        new.activate(point)
                    # otherwiese it stays inactive
            result = new
        return len(result.data)

    def solve1(self):
        return self.solve_(3)

    def solve2(self):
        return self.solve_(4)


Day.main()
