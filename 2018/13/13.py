#!/usr/bin/python

from copy import deepcopy
from itertools import cycle

from advent import Advent

"""
--- Day 13: Mine Cart Madness ---
A crop of this size requires significant logistics to transport produce, soil,
fertilizer, and so on. The Elves are very busy pushing things around in carts on
some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for
another 1000 years, the Elves seem to be making this up as they go along. They
haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections
(+). Curves connect exactly two perpendicular pieces of track; for example, this
is a closed loop:

/----\
|    |
|    |
\----/
Intersections occur when two perpendicular paths cross. At an intersection, a
cart is capable of turning left, turning right, or continuing straight. Here are
two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/
Several carts are also on the tracks. Carts always face either up (^), down (v),
left (<), or right (>). (On your initial map, the track under each cart is a
straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it
turns left the first time, goes straight the second time, turns right the third
time, and then repeats those directions starting again with left the fourth
time, straight the fifth time, and so on. This process is independent of the
particular intersection at which the cart has arrived - that is, the cart has no
per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a
time. They do this based on their current location: carts on the top row move
first (acting from left to right), then carts on the second row move (again from
left to right), then carts on the third row, and so on. Once each cart has moved
one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |
First, the top cart moves. It is facing down (v), so it moves down one square.
Second, the bottom cart moves. It is facing up (^), so it moves up one square.
Because all carts have moved, the first tick ends. Then, the process repeats,
starting with the first cart. The first cart moves down, then the second cart
moves up - right into the first cart, colliding with it! (The location of the
crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/
After following their respective paths for a while, the carts eventually crash.
To help prevent crashes, you'd like to know the location of the first crash.
Locations are given in X,Y coordinates, where the furthest left column is X=0
and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/
In this example, the location of the first crash is 7,3.
"""


N = (0, -1)
S = (0, 1)
W = (-1, 0)
E = (1, 0)
STRAIGHT = 's'
BEND_R = 'r'
BEND_L = 'l'
CROSS = '+'


def move(pos, direction):
    return tuple(map(sum, zip(pos, direction)))


class Cart(object):
    dirtranslation = {
        '^': N,
        'v': S,
        '<': W,
        '>': E,
    }
    turns = {
        'l': {N: W, W: S, S: E, E: N},
        's': {N: N, S: S, E: E, W: W},
        'r': {N: E, E: S, S: W, W: N},
    }

    def __init__(self, x, y, direction, rails):
        self.x = x
        self.y = y
        self.direction = self.dirtranslation[direction]
        self.rails = rails
        self.lsr = cycle('lsr')

    @property
    def pos(self):
        return (self.x, self.y)

    def straight(self):
        self.x, self.y = move(self.pos, self.direction)

    def cross(self):
        t = next(self.lsr)
        self.direction = self.turns[t][self.direction]
        self.straight()

    def bend(self):
        t = self.rails[self.pos]
        # travelling east west, turns are flipped
        if self.direction in (E, W):
            if t == BEND_L:
                t = BEND_R
            else:
                t = BEND_L
        self.direction = self.turns[t][self.direction]
        self.straight()

    def tick(self):
        v = self.rails[self.pos]
        if v == CROSS:
            self.cross()
        elif v in (BEND_R, BEND_L):
            self.bend()
        else:
            assert(v == STRAIGHT)
            self.straight()


class Day(Advent):
    lines = True
    strip = False

    def prepare(self):
        super(Day, self).prepare()
        rails = {}
        carts = []
        for y, line in enumerate(self.data):
            for x, value in enumerate(line):
                if value == ' ':
                    continue
                elif value == '+':
                    rails[(x, y)] = CROSS
                elif value == '/':
                    rails[(x, y)] = BEND_R
                elif value == '\\':
                    rails[(x, y)] = BEND_L
                elif value in '-|':
                    rails[(x, y)] = STRAIGHT
                elif value in '^v<>':
                    rails[(x, y)] = STRAIGHT
                    carts.append(Cart(x, y, value, rails))
                else:
                    raise Exception('failed to parse %s at %s,%s', value, x, y)
        self.rails = rails
        self.carts = carts

    def collissions(self, carts):
        positions = {}
        for cart in carts:
            p = cart.pos
            if p in positions:
                return positions[p], cart
            else:
                positions[p] = cart
        return []

    def solve1(self):
        carts = deepcopy(self.carts)
        while True:
            # need to sort carts in the correct order to iterate them
            for cart in list(sorted(carts, key=lambda c: (c.y, c.x))):
                col = self.collissions(carts)
                if col:
                    return '%s,%s' % col[0].pos
                cart.tick()

    def solve2(self):
        carts = deepcopy(self.carts)
        while len(carts) > 1:
            # need to sort carts in the correct order to iterate them
            for cart in list(sorted(carts, key=lambda c: (c.y, c.x))):
                for col in self.collissions(carts):
                    carts.remove(col)
                cart.tick()
        return '%s,%s' % carts[0].pos


Day.main()
