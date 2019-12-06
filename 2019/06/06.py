#!/usr/bin/pypy3

import re
from advent import Advent

"""
--- Day 6: Universal Orbit Map ---
You've landed at the Universal Orbit Map facility on Mercury. Because navigation
in space often involves transferring between orbits, the orbit maps here are
useful for finding efficient routes between, for example, you and Santa. You
download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit
around exactly one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /
In this diagram, the object BBB is in orbit around AAA. The path that BBB takes
around AAA (drawn with lines) is only partly shown. In the map data, this
orbital relationship is written AAA)BBB, which means "BBB is in orbit around
AAA".

Before you use your map data to plot a course, you need to make sure it wasn't
corrupted during the download. To verify maps, the Universal Orbit Map facility
uses orbit count checksums - the total number of direct orbits (like the one
shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can
be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A
indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
In this visual representation, when two objects are connected by a line, the one
on the right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7
orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?
"""

class Node(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

#    def __hash__(self):
#        return self.name


class Day(Advent):
    matrix = True
    seperator = re.compile(r'\)')

    def prepare(self):
        super(Day, self).prepare()
        self.nodes = {}
        for a, b in self.data:
            if a not in self.nodes:
                self.nodes[a] = Node(a)
            node_a = self.nodes[a]
            if b not in self.nodes:
                self.nodes[b] = Node(b)
            node_b = self.nodes[b]
            assert(node_b.parent is None)
            node_b.parent = node_a
        self.root = None
        for k, v in self.nodes.items():
            if v.parent is None:
                assert(self.root is None)
                self.root = v

    def solve1(self):
        result = 0
        for node in self.nodes.values():
            n = node
            orbits = 0
            while n.parent is not None:
                n = n.parent
                orbits += 1
            result += orbits
        return result

    def trace(self, start):
        node = start
        result = []
        while node.parent is not None:
            result.append(node.name)
            node = node.parent
        result.append(node.name)  # root node
        return result

    def solve2(self):
        you = self.nodes['YOU']
        san = self.nodes['SAN']
        path_you = self.trace(you)
        path_san = self.trace(san)
        diff = []
        for n in path_you + path_san:
            if n in path_you and n in path_san:
                continue  # common
            diff.append(n)
        result = len(diff) - 2  # minus YOU and SAN
        return result


Day.main()
