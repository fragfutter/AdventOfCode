#!/usr/bin/pypy3

from string import ascii_uppercase
from collections import defaultdict

from advent import Advent
from advent.grid import Point
from advent.astar import Astar, Node

"""
"""

FREE = '.'
WALL = '#'

class GridNode(Node):
    def __init__(self, point):
        self.x = point.x
        self.y = point.y
        self.cost = 0
        self.parent = None
        self.data = []

    @property
    def neighbours(self):
        return self.data

    def weight(self, other):
        assert(other in self.data)
        return 1

    def distance(self, other):
        # we have a portals we are not allowed to over estimate
        return 1

    def __repr__(self):
        return '<GridNode %d,%d>' % (self.x, self.y)


class Nodes(object):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        # key is Point(x, y)
        try:
            return self.data[key]
        except KeyError:
            result = GridNode(key)
            self.data[key] = result
            return result

    def __setitem__(self, key, value):
        self.data[key] = value


class Day(Advent):
    lines = True
    strip = False

    def prepare(self):
        super(Day, self).prepare()
        grid = {}
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                if c in (' ', WALL):
                    continue
                p = Point(x, -y)  # top-left => 0,0 ; bottom-right => 50, -50
                grid[p] = c
        # resolve portals
        portals = {}  # lookup label => [p1, p2]
        for p, v in grid.items():
            if v not in ascii_uppercase:
                continue
            s = p.south()
            n = p.north()
            e = p.east()
            w = p.west()
            sc = grid.get(s, '')
            nc = grid.get(n, '')
            ec = grid.get(e, '')
            wc = grid.get(w, '')
            if nc in ascii_uppercase and sc == FREE:
                label = nc + v
                coordinates = s
            elif sc in ascii_uppercase and nc == FREE:
                label = v + sc
                coordinates = n
            elif wc in ascii_uppercase and ec == FREE:
                label = wc + v
                coordinates = e
            elif ec in ascii_uppercase and wc == FREE:
                label = v + ec
                coordinates = w
            else:
                # not the char leading to the portal
                continue
            # remember for fast lookup
            if label in portals:
                portals[label].append(coordinates)
            else:
                portals[label] = [coordinates, ]
        # drop all single uppercase letters, leftover from resolved labels
        for p, v in list(grid.items()):
            if v in ascii_uppercase:
                del grid[p]
        # update grid to have labels on field
        for label, points in portals.items():
            for p in points:
                grid[p] = label
        # generate nodes with neighbours
        nodes = Nodes()
        for p, v in grid.items():
            node = nodes[p]
            for n in p.neighbours(diagonal = False):
                nv = grid.get(n, None)
                if nv is None:
                    continue
                node.data.append(nodes[n])
            # if we are a label, the other label is our neighbour
            if len(v) == 2:
                try:
                    p1, p2 = portals[v]
                except ValueError:
                    # portal leads nowhere
                    continue
                if p == p1:
                    node.data.append(nodes[p2])
                else:
                    node.data.append(nodes[p1])
        self.grid = grid
        self.nodes = nodes
        self.portals = portals

    def solve1(self):
        start = self.nodes[self.portals['AA'][0]]
        end = self.nodes[self.portals['ZZ'][0]]
        astar = Astar(start, end)
        result = astar.solve()
        steps = 0
        while result:
            steps += 1
            result = result.parent
        return steps - 1

    def solve2(self):
        pass


Day.main()
