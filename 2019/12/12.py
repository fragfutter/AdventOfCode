#!/usr/bin/pypy3

import re
import math
from itertools import permutations
from advent import Advent

"""
--- Day 12: The N-Body Problem ---
The space near Jupiter is not a very safe place; you need to be careful of a big
distracting red spot, extreme radiation, and a whole lot of moons swirling
around. You decide to start by tracking the four largest moons: Io, Europa,
Ganymede, and Callisto.

After a brief scan, you calculate the position of each moon (your puzzle input).
You just need to simulate their motion so you can avoid them.

Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional
velocity. The position of each moon is given in your scan; the x, y, and z
velocity of each moon starts at 0.

Simulate the motion of the moons in time steps. Within each time step, first
update the velocity of every moon by applying gravity. Then, once all moons'
velocities have been updated, update the position of every moon by applying
velocity. Time progresses by one step once all of the positions are updated.

To apply gravity, consider every pair of moons. On each axis (x, y, and z), the
velocity of each moon changes by exactly +1 or -1 to pull the moons together.
For example, if Ganymede has an x position of 3, and Callisto has a x position
of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x
velocity changes by -1 (because 3 < 5). However, if the positions on a given
axis are the same, the velocity on that axis does not change for that pair of
moons.

Once all gravity has been applied, apply velocity: simply add the velocity of
each moon to its own position. For example, if Europa has a position of x=1,
y=2, z=3 and a velocity of x=-2, y=0,z=3, then its new position would be x=-1,
y=2, z=6. This process does not modify the velocity of any moon.

Then, it might help to calculate the total energy in the system. The total
energy for a single moon is its potential energy multiplied by its kinetic
energy. A moon's potential energy is the sum of the absolute values of its x, y,
and z position coordinates. A moon's kinetic energy is the sum of the absolute
values of its velocity coordinates. Below, each line shows the calculations for
a moon's potential energy (pot), kinetic energy (kin), and total energy:

What is the total energy in the system after simulating the moons given in your
scan for 1000 steps?

--- Part Two ---
All this drifting around in space makes you wonder about the nature of the
universe. Does history really repeat itself? You're curious whether the moons
will ever return to a previous state.

Determine the number of steps that must occur before all of the moons' positions
and velocities exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly match
a previous point in time; it eventually returns to the initial state:
"""

def cmp(a, b):
    if a > b:
        return 1
    if a < b:
        return -1
    return 0


class Moon(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def gravity(self, other):
        self.vx -= cmp(self.x, other.x)
        self.vy -= cmp(self.y, other.y)
        self.vz -= cmp(self.z, other.z)

    def velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def potential(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def energy(self):
        return self.potential() * self.kinetic()

    def clone(self):
        return Moon(self.x, self.y, self.z)

    def state(self):
        return (self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def __repr__(self):
        return '<Moon x=%d, y=%d, z=%d, vx=%d, vy=%d, vz=%d, energy=%d>' % \
            (self.x, self.y, self.z, self.vx, self.vy, self.vz, self.energy())


class Axis(object):
    def __init__(self, x):
        self.x = x
        self.v = 0

    def gravity(self, other):
        self.v -= cmp(self.x, other.x)

    def velocity(self):
        self.x += self.v

    def state(self):
        return (self.x, self.v)


def lcm(a, b):
    """least common multiple.

    gcd = greatest common divisor

    a * b = lcd(a, b) * gcd(a, b)

    https://www.calculatorsoup.com/calculators/math/lcm.php

    and lcm(a, b, c) = lcm( lcm(a,b), c)
    """
    gcd = math.gcd(a, b)
    return int(a * b / gcd)

class Day(Advent):
    lines = True

    def prepare(self):
        super(Day, self).prepare()
        pat = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
        result = []
        for line in self.data:
            m = pat.match(line)
            args = list(map(int, m.groups()))
            moon = Moon(*args)
            result.append(moon)
        self.data = result

    def step(self, moons):
        for a, b in permutations(moons, 2):
            a.gravity(b)
        for m in moons:
            m.velocity()

    def dump(self, moons):
        for m in moons:
            print(m)

    def solve1(self):
        data = [m.clone() for m in self.data]
        for i in range(1000):
            self.step(data)
        result = sum([m.energy() for m in data])
        return result

    def find_loop(self, *values):
        data = [Axis(v) for v in values]
        step = 0
        initial_state = [m.state() for m in data]
        while True:
            step += 1
            self.step(data)
            state = [m.state() for m in data]
            if state == initial_state:
                return step

    def solve2(self):
        x = [m.x for m in self.data]
        loop_x = self.find_loop(*x)
        y = [m.y for m in self.data]
        loop_y = self.find_loop(*y)
        z = [m.z for m in self.data]
        loop_z = self.find_loop(*z)
        result = lcm( lcm( loop_x, loop_y), loop_z)
        return result


Day.main()
