#!/usr/bin/pypy3

from advent import Advent
from advent.grid import Point
import re

"""
--- Day 3: Crossed Wires ---
The gravity assist was successful, and you're well on your way to the Venus
refuelling station. During the rush back on Earth, the fuel management system
wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are
connected to a central port and extend outward on a grid. You trace the path
each wire takes as it leaves the central port, one wire per line of text (your
puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the
circuit, you need to find the intersection point closest to the central port.
Because the wires are on a grid, use the Manhattan distance for this
measurement. While the wires do technically cross right at the central port
where they both start, this point does not count, nor does a wire count as
crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the
central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?
"""

class Day(Advent):
    matrix = True
    seperator = re.compile(',')
    mapping = {
        'U': 'north',
        'D': 'south',
        'L': 'east',
        'R': 'west',
    }

    def conversion(self, x):
        return (self.mapping[x[0]], int(x[1:]))

    def prepare(self):
        super(Day, self).prepare()

    def trace(self, line):
        result = []
        pos = Point(0, 0)
        for d, steps in line:
            while steps > 0:
                pos = getattr(pos, d)()
                steps -= 1
                result.append(pos)
        return result

    def solve1(self):
        print('tracing a')
        a = self.trace(self.data[0])
        print('tracing b')
        b = self.trace(self.data[1])
        print('searching cross')
        zero = Point(0, 0)
        result = 9999999
        for x in a:
            if x in b:
                d = x.distance(zero)
                if d < result:
                    result = d
        return result

    def solve3(self):
        computer = Intcode(self.data)
        for noun in range(100):
            for verb in range(100):
                if computer.run(noun, verb) == 19690720:
                    return 100 * noun + verb


Day.main()
