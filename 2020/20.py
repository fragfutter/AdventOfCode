#!/usr/bin/pypy3

from advent import Advent
import re

"""
"""

class Tile(object):
    def __init__(self, number):
        self.number = number
        self.data = []

    @property
    def top(self):
        return self.data[0]

    @property
    def bottom(self):
        return self.data[-1]

    @property
    def left(self):
        return ''.join([line[0] for line in self.data])

    @property
    def right(self):
        return ''.join([line[-1] for line in self.data])

    def rotate(self):
        """return copy of self rotated clockwise"""
        pass

    def flip(self):
        """return copy of self flipped around horizontal axis"""
        pass

    def mutations(self):
        """calculate all borders in any mutation"""
        result = []
        result.append(self.top)
        result.append(self.bottom)
        result.append(self.left)
        result.append(self.right)
        # flipping and rotating results in the reverse
        for edge in result[:]:
            result.append(''.join(reversed(edge)))
        return result


class Day(Advent):
    def prepare(self):
        tiles = []
        tile = None
        for line in self.data.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('Tile'):
                number = int(line[5:9])
                if tile:
                    tiles.append(tile)
                tile = Tile(number)
            else:
                tile.data.append(line)
        if tile:
            tiles.append(tile)
        self.data = tiles

    def solve1(self):
        def search(number, side):
            for n, m in mutations.items():
                if side in m and number != n:
                    return n  # tile n matches in some rotation/flip

        mutations = {}
        for tile in self.data:
            mutations[tile.number] = tile.mutations()
        # now iterate over all tiles and find tile where two edges are
        # not available as mutation
        corners = []
        for tile in self.data:
            matches = []
            for side in tile.top, tile.right, tile.bottom, tile.left:
                matches.append(search(tile.number, side))
            if matches.count(None) == 2:
                corners.append(tile.number)
        result = 1
        for corner in corners:
            result *= corner
        return result

    def solve2(self):
        pass


Day.main()
