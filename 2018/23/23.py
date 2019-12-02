#!/usr/bin/python

import re
from collections import namedtuple
from heapq import heappush, heappop
import math
import logging

from advent import Advent

"""
--- Day 23: Experimental Emergency Teleportation ---
Using your torch to search the darkness of the rocky cavern, you finally locate
the man's friend: a small reindeer.

You're not sure how it got so far in this cave. It looks sick - too sick to walk
- and too heavy for you to carry all the way back. Sleighs won't be invented for
another 1500 years, of course.

The only option is experimental emergency teleportation.

You hit the "experimental emergency teleportation" button on the device and push
I accept the risk on no fewer than 18 different warning messages. Immediately,
the device deploys hundreds of tiny nanobots which fly around the cavern,
apparently assembling themselves into a very specific formation. The device
lists the X,Y,Z position (pos) for each nanobot as well as its signal radius (r)
on its tiny screen (your puzzle input).

Each nanobot can transmit signals to any integer coordinate which is a distance
away from it less than or equal to its signal radius (as measured by Manhattan
distance). Coordinates a distance away of less than or equal to a nanobot's
signal radius are said to be in range of that nanobot.

Before you start the teleportation process, you should determine which nanobot
is the strongest (that is, which has the largest signal radius) and then, for
that nanobot, the total number of nanobots that are in range of it, including
itself.

For example, given the following nanobots:

  pos=<0,0,0>, r=4
  pos=<1,0,0>, r=1
  pos=<4,0,0>, r=3
  pos=<0,2,0>, r=1
  pos=<0,5,0>, r=3
  pos=<0,0,3>, r=1
  pos=<1,1,1>, r=1
  pos=<1,1,2>, r=1
  pos=<1,3,1>, r=1

The strongest nanobot is the first one (position 0,0,0) because its signal
radius, 4 is the largest. Using that nanobot's location and signal radius, the
following nanobots are in or out of range:

  The nanobot at 0,0,0 is distance 0 away, and so it is in range.
  The nanobot at 1,0,0 is distance 1 away, and so it is in range.
  The nanobot at 4,0,0 is distance 4 away, and so it is in range.
  The nanobot at 0,2,0 is distance 2 away, and so it is in range.
  The nanobot at 0,5,0 is distance 5 away, and so it is not in range.
  The nanobot at 0,0,3 is distance 3 away, and so it is in range.
  The nanobot at 1,1,1 is distance 3 away, and so it is in range.
  The nanobot at 1,1,2 is distance 4 away, and so it is in range.
  The nanobot at 1,3,1 is distance 5 away, and so it is not in range.

In this example, in total, 7 nanobots are in range of the nanobot with the
largest signal radius.

Find the nanobot with the largest signal radius. How many nanobots are in range
of its signals?  """

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def neighbours(x, y, z, offset=1):
    yield (x + offset, y, z)
    yield (x - offset, y, z)
    yield (x, y + offset, z)
    yield (x, y - offset, z)
    yield (x, y, z + offset)
    yield (x, y, z - offset)


class Bot(namedtuple('Bot', ['x', 'y', 'z', 'r'])):
    def distance(self, other):
        return abs(self.x - other.x) + \
            abs(self.y - other.y) + \
            abs(self.z - other.z)

    def in_range(self, other):
        return self.distance(other) <= self.r

    def coordinates(self):
        return (self.x, self.y, self.z)

    def reach(self):
        coo = self.coordinates()
        seen = []
        queue = [coo]
        while queue:
            result = queue.pop(0)
            if result in seen:
                continue
            seen.append(result)
            yield result
            for n in neighbours(*result):
                if n in seen:
                    continue
                if sum([abs(x - y) for x, y in zip(coo, n)]) > self.r:
                    continue
                queue.append(n)

    def count(self, bots):
        """number of bots that can reach my position"""
        return sum([other.in_range(self) for other in bots])


class Day(Advent):
    lines = True
    pat = re.compile('pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$')

    @classmethod
    def conversion(cls, line):
        try:
            data = map(int, cls.pat.match(line).groups())
        except:
            print(line)
            raise
        return Bot(*data)

    def prepare(self):
        super(Day, self).prepare()

    def solve1(self):
        t = sorted(self.data, key=lambda x: x.r, reverse=True)[0]
        result = 0
        for o in self.data:
            if t.in_range(o):
                result += 1
        return result

    def solve2(self):
        total_bots = len(self.data)
        center = Bot(0, 0, 0, 0)
        max_rad = max([bot.distance(center) for bot in self.data])
        #  make it a power of 2
        r = int(math.pow(2, math.ceil(math.log2(max_rad))))
        # total_bots - bots_in_area
        # distance to 0,0,0
        # radius
        # the bot data
        heap = []
        init = Bot(0, 0, 0, r)
        heappush(
            heap,
            (
                total_bots - init.count(self.data),
                init.distance(center),
                init.r,
                init
            )
        )
        while heap:
            log.debug(heap)
            log.debug(str(heap[0]))
            _, _, _, b = heappop(heap)
            if b.r == 1:
                return str(b)
            # slice it
            r = b.r // 2
            offset = r // 2
            if offset == 0:
                offset = 1
            for x, y, z in neighbours(b.x, b.y, b.z, offset):
                n = Bot(x, y, z, r)
                heappush(
                    heap,
                    (
                        total_bots - n.count(self.data),
                        n.distance(center),
                        n.r,
                        n
                    )
                )
            n = Bot(b.x, b.y, b.z, r)
            heappush(
                heap,
                (
                    total_bots - n.count(self.data),
                    n.distance(center),
                    n.r,
                    n
                )
            )


Day.main()
