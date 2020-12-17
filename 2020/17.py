#!/usr/bin/pypy3

from advent import Advent

"""
"""

class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def as_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return str(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return hash(self.as_tuple())

    def neighbours(self):
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    if x==y==z==0:
                        continue
                    yield Point3D(self.x+x, self.y+y, self.z+z)


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
        for x in range(
            min(self.data, key=lambda i: i.x).x - offset,
            max(self.data, key=lambda i: i.x).x + offset + 1):
            for y in range(
                min(self.data, key=lambda i: i.y).y - offset,
                max(self.data, key=lambda i: i.y).y + offset + 1):
                for z in range(
                    min(self.data, key=lambda i: i.z).z - offset,
                    max(self.data, key=lambda i: i.z).z + offset + 1):

                    yield Point3D(x, y, z)

    def count(self, point):
        result = 0
        for n in point.neighbours():
            if n in self.data:
                result += 1
        return result


class Day(Advent):
    matrix = True
    conversion = lambda x: x=='#'

    def prepare(self):
        result = Grid()
        for y, line in enumerate(self.data.split('\n')):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    result.activate(Point3D(x, y, 0))
        self.data = result

    def solve1(self):
        result = self.data
        for i in range(6):
            new = Grid()
            for point in result.iterate():
                count = result.count(point)
                if point in result.data:
                    if count in (2, 3):
                        new.activate(point)
                else:
                    if count == 3:
                        new.activate(point)
            result = new
        return len(result.data)

    def solve2(self):
        pass


Day.main()
