#!/usr/bin/python

from collections import defaultdict

from advent import Advent

"""
--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like
you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal
interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they
places it thinks are safe or dangerous? It recommends you check manual page
729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the
coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by
counting the number of integer X,Y locations that are closest to that
coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For
example, consider the following list of coordinates:

  1, 1
  1, 6
  8, 3
  3, 4
  5, 5
  8, 9

If we name these coordinates A through F, we can draw them on a grid, putting
0,0 at the top left:

  ..........
  .A........
  ..........
  ........C.
  ...D......
  .....E....
  .B........
  ..........
  ..........
  ........F.

This view is partial - the actual grid extends infinitely in all directions.
Using the Manhattan distance, each location's closest coordinate can be
determined, shown here in lowercase:

  aaaaa.cccc
  aAaaa.cccc
  aaaddecccc
  aadddeccCc
  ..dDdeeccc
  bb.deEeecc
  bBb.eeee..
  bbb.eeefff
  bbb.eeffff
  bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they
don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while
not shown here, their areas extend forever outside the visible grid. However,
the areas of coordinates D and E are finite: D is closest to 9 locations, and E
is closest to 17 (both including the coordinate's location itself). Therefore,
in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

"""


class Point(object):
    _name = 1

    def __init__(self, x, y, distance, name=None):
        self.x = x
        self.y = y
        if name is None:
            self.__class__._name += 1
            name = self.__class__._name
        self.name = name
        self.distance = distance

    def __repr__(self):
        return '(name=%s, x=%s, y=%s, d=%s)' % (self.name, self.x, self.y, self.distance)

    @property
    def coordinates(self):
        return (self.x, self.y)

    def neighbours(self):
        d = self.distance + 1
        yield Point(self.x + 1, self.y, d, self.name)
        yield Point(self.x - 1, self.y, d, self.name)
        yield Point(self.x, self.y + 1, d, self.name)
        yield Point(self.x, self.y - 1, d, self.name)


class Grid(object):
    def __init__(self):
        self.data = {}

    def name(self, coordinates):
        point = self.data.get(coordinates, None)
        if point:
            return point.name
        else:
            return None

    def distance(self, coordinates):
        point = self.data.get(coordinates, None)
        if point:
            return point.distance
        else:
            return None

    def better(self, point):
        existing = self.data.get(point.coordinates, None)
        if not existing:
            return True
        if existing.distance > point.distance:
            return True
        if existing.distance < point.distance:
            return False
        assert(existing.distance == point.distance)
        if existing.name == point.name:
            return False  # same owner
        if existing.name == 0:
            return False  # already tied
        # tied, wipe out
        tie = Point(point.x, point.y, point.distance, 0)
        self.set(tie)
        return False

    def set(self, point):
        self.data[point.coordinates] = point

    def areas(self):
        result = defaultdict(lambda: [])
        for point in self.data.values():
            if point.name == 0:
                continue
            result[point.name].append(point)
        return result


class Day(Advent):
    lines = True

    @classmethod
    def conversion(cls, line):
        x, y = tuple(map(int, line.split(', ')))
        return Point(x, y, 0)

    def prepare(self):
        super(Day, self).prepare()

    def solve1(self):
        # extract boundaries
        left = min([p.x for p in self.data])
        right = max([p.x for p in self.data])
        top = min([p.y for p in self.data])
        bottom = max([p.y for p in self.data])
        print(left, right, top, bottom)
        grid = Grid()
        queue = list(self.data)
        while queue:
            p = queue.pop(0)
            if p.x < left or p.x > right or p.y < top or p.y > bottom:
                continue  # infinity point
            if grid.better(p):
                grid.set(p)
                # add neighbours to queue, they have distance + 1
                for n in p.neighbours():
                    queue.append(n)
        # find area sizes
        return max(len(points) for points in grid.areas().values())

    def solve2(self):
        pass


Day.main()
