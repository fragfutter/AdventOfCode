#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

from collections import defaultdict, namedtuple
from advent import Advent

"""
--- Day 17: Reservoir Research ---
You arrive in the year 18. If it weren't for the coat you got in 1018, you would
be very cold: the North Pole base hasn't even been constructed.

Rather, it hasn't been constructed yet. The Elves are making a little progress,
but there's not a lot of liquid water in this climate, so they're getting very
dehydrated. Maybe there's more underground?

You scan a two-dimensional vertical slice of the ground nearby and discover that
it is mostly sand with veins of clay. The scan only provides data with a
granularity of square meters, but it should be good enough to determine how much
water is trapped there. In the scan, x represents the distance to the right, and
y represents the distance down. There is also a spring of water near the surface
at x=500, y=0. The scan identifies which square meters are clay (your puzzle
input).

For example, suppose your scan shows the following veins of clay:

x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
Rendering clay as #, sand as ., and the water spring as +, and with x increasing
to the right and y increasing downward, this becomes:

   44444455555555
   99999900000000
   45678901234567
 0 ......+.......
 1 ............#.
 2 .#..#.......#.
 3 .#..#..#......
 4 .#..#..#......
 5 .#.....#......
 6 .#.....#......
 7 .#######......
 8 ..............
 9 ..............
10 ....#.....#...
11 ....#.....#...
12 ....#.....#...
13 ....#######...
The spring of water will produce water forever. Water can move through sand, but
is blocked by clay. Water always moves down when possible, and spreads to the
left and right otherwise, filling space that has clay on both sides and falling
out otherwise.

For example, if five squares of water are created, they will flow downward until
they reach the clay and settle there. Water that has come to rest is shown here
as ~, while sand through which water has passed (but which is now dry again) is
shown as |:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
Two squares of water can't occupy the same location. If another five squares of
water are created, they will settle on the first five, filling the clay
reservoir a little more:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
Water pressure does not apply in this scenario. If another four squares of water
are created, they will stay on the right side of the barrier, and no water will
reach the left side:

......+.......
......|.....#.
.#..#.|.....#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
At this point, the top reservoir overflows. While water can reach the tiles
above the surface of the water, it cannot settle there, and so the next five
squares of water settle like this:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#...|.#...
....#...|.#...
....#~~~~~#...
....#######...
Note especially the leftmost |: the new squares of water can reach this tile,
but cannot stop there. Instead, eventually, they all fall to the right and
settle in the reservoir down.

After 10 more squares of water, the bottom reservoir is also full:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#~~~~~#...
....#~~~~~#...
....#~~~~~#...
....#######...
Finally, while there is nowhere left for the water to settle, it can reach a few
more tiles before overflowing beyond the bottom of the scanned data:

......+.......    (line not counted: above minimum y value)
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..
...|.......|..    (line not counted: down maximum y value)
...|.......|..    (line not counted: down maximum y value)
...|.......|..    (line not counted: down maximum y value)
How many tiles can be reached by the water? To prevent counting forever, ignore
tiles with a y coordinate smaller than the smallest y coordinate in your scan
data or larger than the largest one. Any x coordinate is valid. In this example,
the lowest y coordinate given is 1, and the highest is 13, causing the water
spring (in row 0) and the water falling off the bottom of the render (in rows 14
through infinity) to be ignored.

So, in the example above, counting both water at rest (~) and other sand tiles
the water can hypothetically reach (|), the total number of tiles the water can
reach is 57.

How many tiles can the water reach within the range of y values in your scan?
"""


class Grid(object):
    def __init__(self):
        self.data = defaultdict(lambda: '.')

    def update_dimensions(self):
        self.min_x = min([p[0] for p in self.data]) - 1
        self.min_y = min([p[1] for p in self.data])
        self.max_x = max([p[0] for p in self.data]) + 2
        self.max_y = max([p[1] for p in self.data])
        log.debug('x: %d .. %d  ; y: %d .. %d',
                  self.min_x, self.max_x, self.min_y, self.max_y)

    def dump(self):
        print()
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                print(self.data[(x, y)], end='')  # noqa
            print()

    def add_clay(self, x1, x2, y1, y2):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.data[(x, y)] = '#'

    def add_water(self):
        self.data[(500, self.min_y)] = '|'
        queue = [(500, self.min_y)]
        while queue:
            # import pdb; pdb.set_trace()
            pos = queue.pop()
            log.debug(pos)
            x, y = pos
            if y == self.max_y:
                continue
            up = (x, y - 1)
            down = (x, y + 1)
            left = (x - 1, y)
            right = (x + 1, y)
            if self.data[pos] == '|':
                if self.data[down] == '.':
                    self.data[down] = '|'
                    queue.append(pos)
                    queue.append(down)
                    continue
                if self.data[down] in ('~', '#'):
                    self.data[pos] = '+'  # spread
                    queue.append(pos)
                    continue
            if self.data[pos] == '+':
                if self.data[left] == '.':
                    self.data[left] = '|'
                    queue.append(pos)  # need to recheck ourself
                    queue.append(left)
                    continue
                if self.data[right] == '.':
                    self.data[right] = '|'
                    queue.append(pos)  # need to recheck ourself
                    queue.append(right)
                    continue
                if self.data[left] == '#':
                    # search to the right for another wall
                    i = x
                    while i < self.max_x:
                        if self.data[(i, y)] != '+':
                            break
                        i += 1
                    if self.data[(i, y)] == '#':
                        # from here to the right all spreading, stand it
                        for j in range(x, i):
                            self.data[(j, y)] = '~'
                if self.data[right] == '#':
                    # search to the right for another wall
                    i = x
                    while i > self.min_x:
                        if self.data[(i, y)] != '+':
                            break
                        i -= 1
                    if self.data[(i, y)] == '#':
                        # from here to the current position all spreading
                        for j in range(i + 1, x + 1):
                            self.data[(j, y)] = '~'

    def count(self):
        result = {
            '.': 0,
            '|': 0,
            '~': 0,
            '+': 0,
            '#': 0,
        }
        for v in self.data.values():
            result[v] += 1
        return result


class Day(Advent):
    lines = True

    def prepare(self):
        def to_list(data):
            if '..' in data:
                return list(map(int, data.split('..')))
            else:
                d = int(data)
                return [d, d]

        super(Day, self).prepare()
        grid = Grid()
        for line in self.data:
            row = []
            x, y = [a.split('=')[1] for a in line.split(', ')]
            if line.startswith('y'):
                x, y = y, x
            row.extend(to_list(x))
            row.extend(to_list(y))
            grid.add_clay(*row)
        grid.update_dimensions()
        self.data = grid

    def solver(self):
        self.data.add_water()
        c = self.data.count()
        return c['|'] + c['~'] + c['+'], c['~']

    def solve2(self):
        pass


Day.main()
