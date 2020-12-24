#!/usr/bin/pypy3

from advent import Advent
from advent.hexgrid import Hex

"""
"""

class Day(Advent):
    def prepare(self):
        result = []
        for line in self.data.split('\n'):
            line = list(line.strip())
            steps = []
            c = line.pop(0)
            while c:
                if c in ('e', 'se', 'sw', 'w', 'nw', 'ne'):
                    steps.append(c)
                    c = ''
                try:
                    c += line.pop(0)
                except IndexError:
                    pass
            assert(c == '')
            result.append(steps)
        self.data = result

    def solve1(self):
        """
        my hexgrid looks like
              \ n  /
            nw +--+ ne
              /    \
            -+      +-
              \    /
            sw +--+ se
              / s  \

        coordinates given are

                +
              /   \
             +     +
             |     |
             +     +
              \   /
                +

        so turn 90 degrees
        """
        translation = {
            'e': 'south',
            'se': 'southwest',
            'sw': 'northwest',
            'w': 'north',
            'nw': 'northeast',
            'ne': 'southeast',
        }
        black = set()
        for steps in self.data:
            cube = Hex(0, 0)
            for step in steps:
                cube = getattr(cube, translation[step])()
            if cube in black:
                black.remove(cube)
            else:
                black.add(cube)
        self.black = black
        return len(black)

    def solve2(self):
        def size(grid):
            q = max([abs(c.q) for c in grid])
            r = max([abs(c.r) for c in grid])
            return max(q, r) + 1


        def day(black):
            # running over a grid that is way too large
            # but lazy, don't want to think about max/min coordinates
            s = size(black)
            result = set()
            for q in range(-s, s + 1):
                for r in range(-s, s + 1):
                    cube = Hex(q, r)
                    # black neighbours
                    n = sum([c in black for c in cube.neighbours()])
                    if cube in black:
                        # black
                        if n == 0 or n > 2:
                            pass  # becomes white
                        else:
                            result.add(cube)  # stays black
                    else:
                        # white
                        if n == 2:
                            result.add(cube)  # becomes black
                        else:
                            pass  # stays white
            return result

        black = self.black
        for i in range(1, 101):
            black = day(black)
        return len(black)


Day.main()
