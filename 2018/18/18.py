#!/usr/bin/python

from copy import deepcopy
from collections import defaultdict

from advent import Advent

"""
--- Day 18: Settlers of The North Pole ---
On the outskirts of the North Pole base construction project, many Elves are
collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be either open
ground (.), trees (|), or a lumberyard (#). You take a scan of the area (your
puzzle input).

Strange magic is at work here: each minute, the landscape looks entirely
different. In exactly one minute, an open acre can fill with trees, a wooded
acre can be converted to a lumberyard, or a lumberyard can be cleared to open
ground (the lumber having been sent to other projects).

The change to each acre is based entirely on the contents of that acre as well
as the number of open, wooded, or lumberyard acres adjacent to it at the start
of each minute. Here, "adjacent" means any of the eight acres surrounding that
acre. (Acres on the edges of the lumber collection area might have fewer than
eight adjacent acres; the missing acres aren't counted.)

In particular:

  - An open acre will become filled with trees if three or more adjacent acres
  contained trees. Otherwise, nothing happens.
  - An acre filled with trees will become a lumberyard if three or more adjacent
  acres were lumberyards. Otherwise, nothing happens.
  - An acre containing a lumberyard will remain a lumberyard if it was adjacent
  to at least one other lumberyard and at least one acre containing trees.
  Otherwise, it becomes open.

These changes happen across all acres simultaneously, each of them using the
state of all acres at the beginning of the minute and changing to their new form
by the end of that same minute.  Changes that happen during the minute don't
affect each other.

For example, suppose the lumber collection area is instead only 10 by 10 acres
with this initial configuration:

  Initial state:
  .#.#...|#.
  .....#|##|
  .|..|...#.
  ..|#.....#
  #.#|||#|#|
  ...#.||...
  .|....|...
  ||...#|.#|
  |.||||..|.
  ...#.|..|.

  After 1 minute:
  .......##.
  ......|###
  .|..|...#.
  ..|#||...#
  ..##||.|#|
  ...#||||..
  ||...|||..
  |||||.||.|
  ||||||||||
  ....||..|.

  After 2 minutes:
  .......#..
  ......|#..
  .|.|||....
  ..##|||..#
  ..###|||#|
  ...#|||||.
  |||||||||.
  ||||||||||
  ||||||||||
  .|||||||||

  After 3 minutes:
  .......#..
  ....|||#..
  .|.||||...
  ..###|||.#
  ...##|||#|
  .||##|||||
  ||||||||||
  ||||||||||
  ||||||||||
  ||||||||||

  After 4 minutes:
  .....|.#..
  ...||||#..
  .|.#||||..
  ..###||||#
  ...###||#|
  |||##|||||
  ||||||||||
  ||||||||||
  ||||||||||
  ||||||||||

  After 5 minutes:
  ....|||#..
  ...||||#..
  .|.##||||.
  ..####|||#
  .|.###||#|
  |||###||||
  ||||||||||
  ||||||||||
  ||||||||||
  ||||||||||

  After 6 minutes:
  ...||||#..
  ...||||#..
  .|.###|||.
  ..#.##|||#
  |||#.##|#|
  |||###||||
  ||||#|||||
  ||||||||||
  ||||||||||
  ||||||||||

  After 7 minutes:
  ...||||#..
  ..||#|##..
  .|.####||.
  ||#..##||#
  ||##.##|#|
  |||####|||
  |||###||||
  ||||||||||
  ||||||||||
  ||||||||||

  After 8 minutes:
  ..||||##..
  ..|#####..
  |||#####|.
  ||#...##|#
  ||##..###|
  ||##.###||
  |||####|||
  ||||#|||||
  ||||||||||
  ||||||||||

  After 9 minutes:
  ..||###...
  .||#####..
  ||##...##.
  ||#....###
  |##....##|
  ||##..###|
  ||######||
  |||###||||
  ||||||||||
  ||||||||||

  After 10 minutes:
  .||##.....
  ||###.....
  ||##......
  |##.....##
  |##.....##
  |##....##|
  ||##.####|
  ||#####|||
  ||||#|||||
  ||||||||||

After 10 minutes, there are 37 wooded acres and 31 lumberyards. Multiplying the
number of wooded acres by the number of lumberyards gives the total resource
value after ten minutes: 37 * 31 = 1147.

What will the total resource value of the lumber collection area be after 10
minutes?

--- Part Two ---
This important natural resource will need to last for at least thousands of
years. Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after
1000000000 minutes?
"""


OPEN = '.'
TREE = '|'
YARD = '#'


def neighbours(pos):
    x, y = pos
    yield (x, y - 1)
    yield (x + 1, y - 1)
    yield (x + 1, y)
    yield (x + 1, y + 1)
    yield (x, y + 1)
    yield (x - 1, y + 1)
    yield (x - 1, y)
    yield (x - 1, y - 1)


def count_type(data, type_):
    return len(list(filter(lambda x: x == type_, data)))


class Day(Advent):
    lines = True

    def prepare(self):
        super(Day, self).prepare()
        grid = defaultdict(lambda: None)
        for y, line in enumerate(self.data):
            for x, value in enumerate(line):
                grid[(x, y)] = value
        self.data = grid

    def mutate(self, grid):
        new = deepcopy(grid)
        for pos, value in list(grid.items()):
            adjacent = [grid[x] for x in neighbours(pos)]
            if value == OPEN:
                if count_type(adjacent, TREE) >= 3:
                    new[pos] = TREE
            elif value == TREE:
                if count_type(adjacent, YARD) >= 3:
                    new[pos] = YARD
            elif value == YARD:
                if YARD in adjacent and TREE in adjacent:
                    pass
                else:
                    new[pos] = OPEN
        return new

    def solve1(self):
        i = 10
        grid = deepcopy(self.data)
        while i > 0:
            grid = self.mutate(grid)
            i -= 1
        return count_type(grid.values(), TREE) * count_type(grid.values(), YARD)

    def solve2(self):
        i = 1000000000
        cache = {}
        grid = deepcopy(self.data)
        while i > 0:
            key = tuple(grid.items())
            if key in cache:
                loopsize = cache[key] - i
                print('loop detected', loopsize)
                # now jump in loops
                while i > loopsize:
                    i -= loopsize
                # wipe cache to run the rest
                cache = {}
            else:
                cache[key] = i
            grid = self.mutate(grid)
            i -= 1
        return count_type(grid.values(), TREE) * count_type(grid.values(), YARD)


Day.main()
