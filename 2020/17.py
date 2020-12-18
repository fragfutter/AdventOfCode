#!/usr/bin/pypy3

from advent import Advent

"""
"""

class Point(object):
    def __init__(self, *coordinates):
        self.coordinates = tuple(coordinates)

    def as_tuple(self):
        return self.coordinates

    def __repr__(self):
        return str(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return hash(self.as_tuple())

    def dimensions(self):
        return len(self.coordinates)

    def neighbours_dimensions(self, dimension):
        """yield neighbours for dimension"""
        if dimension >= len(self.coordinates):
            yield self
            return  # terminate iteration
        coordinates = list(self.coordinates)
        for i in (-1, 0, 1):
            coordinates[dimension] = i
            point = Point(*coordinates)
            for p in point.neighbours_dimensions(dimension + 1):
                yield p

    def neighbours(self):
        def recursion(dimension):
            if not dimension:
                # final
                yield ()
                return
            for outer in recursion(dimension - 1):
                start = self.coordinates[dimension - 1] - 1
                stop = self.coordinates[dimension - 1] + 1
                for inner in range(start, stop + 1):
                    coordinates = outer + (inner, )
                    yield coordinates

        for coordinates in recursion(self.dimensions()):
            if coordinates != self.coordinates:
                yield Point(*coordinates)


class Grid(object):
    def __init__(self, points=[]):
        self.data = []
        for point in points:
            self.activate(point)

    def activate(self, point):
        if point not in self.data:
            self.data.append(point)

    def deactivate(self, point):
        try:
            self.data.remove(point)
        except ValueError:
            pass

    def iterate(self, offset=1):
        def recursion(dimension):
            if not dimension:
                # final
                yield ()
                return
            for outer in recursion(dimension - 1):
                start = min(map(lambda point: point.coordinates[dimension - 1], self.data)) - offset
                stop  = max(map(lambda point: point.coordinates[dimension - 1], self.data)) + offset
                for inner in range(start, stop + 1):
                    coordinates = outer + (inner, )
                    yield coordinates

        dimension = self.data[0].dimensions()
        for coordinates in recursion(dimension):
            yield Point(*coordinates)

    def count_neighbours(self, point):
        result = 0
        for n in point.neighbours():
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
                    result.append(Point(x, y))
        self.data = result

    def solve_(self, dimensions):
        extension = (0, ) * (dimensions - 2)
        result = Grid()
        for point in self.data:
            coordinates = point.coordinates + extension
            result.activate(Point(*coordinates))
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
        import profile
        profile.runctx('self.solve_(3)', globals(), locals())


Day.main()
