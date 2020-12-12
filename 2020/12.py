#!/usr/bin/pypy3

from advent import Advent
import cmath

"""
"""

directions = {
    'N': complex(0, 1),
    'S': complex(0, -1),
    'E': complex(1, 0),
    'W': complex(-1, 0),
}
rotation = {
    'R': complex(0, -1),
    'L': complex(0, 1),
}

class Day(Advent):
    lines = True

    def solve1(self):
        d = directions['E']
        p = complex(0, 0)

        for value in self.data:
            a = value[0]
            v = int(value[1:])
            if a in directions:
                p += directions[a] * v
                continue
            if a in rotation:
                d = d * rotation[a] ** (v/90)
                continue
            assert(a == 'F')
            p += d * v

        return int(abs(p.real) + abs(p.imag))

    def solve2(self):
        p = complex(0, 0)
        w = complex(10, 1)

        for value in self.data:
            a = value[0]
            v = int(value[1:])
            if a in directions:
                w += directions[a] * v
                continue
            if a in rotation:
                w = w * rotation[a] ** (v/90)
                continue
            assert(a == 'F')
            p += w * v

        return int(abs(p.real) + abs(p.imag))


Day.main()
