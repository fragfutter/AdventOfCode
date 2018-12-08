#!/usr/bin/python

import re
from collections import namedtuple
from collections import defaultdict

from advent import Advent

"""
--- Day 3: No Matter How You Slice It ---
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's
suit (thanks to someone who helpfully wrote its box IDs on the wall of the
warehouse in the middle of the night). Unfortunately, anomalies are still
affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least
1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's
suit. All claims have an ID and consist of a single rectangle with edges
parallel to the edges of the fabric. Each claim's rectangle is defined as
follows:

  - The number of inches between the left edge of the fabric and the left edge
    of the rectangle.
  - The number of inches between the top edge of the fabric and the top edge of
    the rectangle.
  - The width of the rectangle in inches.
  - The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3
inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4
inches tall. Visually, it claims the square inches of fabric represented by #
(and ignores the square inches of fabric represented by .) in the diagram below:

  ...........
  ...........
  ...#####...
  ...#####...
  ...#####...
  ...#####...
  ...........
  ...........
  ...........

The problem is that many of the claims overlap, causing two or more claims to
cover part of the same areas. For example, consider the following claims:

  #1 @ 1,3: 4x4
  #2 @ 3,1: 4x4
  #3 @ 5,5: 2x2

Visually, these claim the following areas:

  ........
  ...2222.
  ...2222.
  .11XX22.
  .11XX22.
  .111133.
  .111133.
  ........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3,
while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough
fabric. How many square inches of fabric are within two or more claims?
"""


fields = ['id', 'left', 'top', 'width', 'height']
Rect = namedtuple('Rect', fields)


class Day(Advent):
    lines = True
    pat = re.compile(r'^#(\d+)\s@\s(\d+),(\d+): (\d+)x(\d+)$')

    @classmethod
    def conversion(cls, line):
        data = dict(
            zip(
                fields,
                map(int, cls.pat.match(line).groups())
            )
        )
        return Rect(**data)

    def rect_coordinates(self, rect):
        for x in range(rect.left, rect.left + rect.width):
            for y in range(rect.top, rect.top + rect.height):
                yield (x, y)

    def prepare(self):
        super(Day, self).prepare()
        grid = defaultdict(lambda: 0)
        for rect in self.data:
            for coordinates in self.rect_coordinates(rect):
                grid[coordinates] += 1
        self.grid = grid

    def solve1(self):
        result = 0
        for point in self.grid.values():
            if point > 1:
                result += 1
        return result
        # one liners too count values > 0
        # return len(list(filter(lambda x: x > 1, grid.values())))
        # return sum([1 if x > 1 else 0 for x in grid.values()])

    def solve2(self):
        result = [x.id for x in self.data]
        for rect in self.data:
            for coordinates in self.rect_coordinates(rect):
                if self.grid[coordinates] > 1:
                    result.remove(rect.id)
                    break
        assert(len(result) == 1)
        return result[0]


Day.main()
