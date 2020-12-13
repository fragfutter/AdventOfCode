#!/usr/bin/pypy3

from advent import Advent
from functools import reduce

"""
"""

class Day(Advent):
    lines = True
    conversion = int

    def prepare(self):
        data = list(self.data.split('\n'))
        self.timestamp = int(data[0])
        result = {}
        for interval, bus in enumerate(data[1].split(',')):
            try:
                bus = int(bus)
                result[bus] = interval
            except ValueError:
                pass
        self.busses = result
        print(self.busses)

    def solve1(self):
        timestamp = self.timestamp
        while True:
            for bus in self.busses.keys():
                if timestamp % bus == 0:
                    return bus * (timestamp - self.timestamp)
            timestamp += 1

    def solve2(self):
        busses = [(bus, interval) for bus, interval in self.busses.items()]
        jump = 1
        timestamp = 0
        for bus, interval in busses:
            while (timestamp + interval) % bus != 0:
                timestamp += jump
            jump = jump * bus
        return timestamp


Day.main()
