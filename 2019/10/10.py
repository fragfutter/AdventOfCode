#!/usr/bin/pypy3

from advent import Advent

"""
--- Day 10: Monitoring Station ---
You fly into the asteroid belt and reach the Ceres monitoring station. The
Elves here have an emergency: they're having trouble tracking all of the
asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of
space; they hand you a map of all of the asteroids in that region (your puzzle
input).

The map indicates whether each position is empty (.) or contains an asteroid
(#). The asteroids are much smaller than they appear on the map, and every
asteroid is exactly in the center of its marked position. The asteroids can be
described with X,Y coordinates where X is the distance from the left edge and Y
is the distance from the top edge (so the top-left corner is 0,0 and the
position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a new
monitoring station. A monitoring station can detect any asteroid to which it
has direct line of sight - that is, there cannot be another asteroid exactly
between them. This line of sight can be at any angle, not just lines aligned to
the grid or diagonally. The best location is the asteroid that can detect the
largest number of other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##

The best location for a new monitoring station on this map is the highlighted
asteroid at 3,4 because it can detect 8 asteroids, more than any other
location. (The only asteroid it cannot detect is the one at 1,0; its view of
this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse
locations; they can detect 7 or fewer other asteroids. Here is the number of
other asteroids a monitoring station on each asteroid could detect:

.7..7
.....
67775
....7
...87

Here is an asteroid (#) and some examples of the ways its line of sight might
be blocked. If there were another asteroid at the location of a capital letter,
the locations marked with the corresponding lowercase letter would be blocked
and could not be detected:

#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c

Here are some larger examples:

Best is 5,8 with 33 other asteroids detected:

......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####

Best is 1,2 with 35 other asteroids detected:

#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.

Best is 6,3 with 41 other asteroids detected:

.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..

Best is 11,13 with 210 other asteroids detected:

.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##

Find the best location for a new monitoring station. How many other asteroids can be detected from that location?
"""


def divisors(a):
    """yield all factors of a"""
    a = abs(a)
    for i in range(1, a//2 + 1):
        if a % i == 0:
            yield i
    yield a


def raytrace(a, b):
    """all integer points between a and b"""
    d = b - a
    limit = int(max(abs(d.real), abs(d.imag)))
    for l in range(limit, 1, -1):
        r = d / l
        if r.real != int(r.real):
            continue
        if r.imag != int(r.imag):
            continue
        # l is a integer divisor of the distance
        # vector r is a stepper
        for i in range(1, l):
            yield a + i * r


class Day(Advent):
    lines = True

    def prepare(self):
        super(Day, self).prepare()
        self.maxx = len(self.data[0])
        self.maxy = len(self.data)
        result = []
        for y, line in enumerate(self.data):
            for x, value in enumerate(line):
                if value == '#':
                    result.append(complex(x, y))
        self.data = result

    def solve1(self):
        result = (0, None)  # visible from location
        for m in self.data:
            visible = 0
            for other in self.data:
                if m == other:
                    continue
                for check in raytrace(m, other):
                    if check in self.data:
                        break  # meteor check will hide other
                else:
                    visible += 1  # not hidden by anyone
            if visible > result[0]:
                result = (visible, m)
        return result[0]

    def solve2(self):
        pass


Day.main()
