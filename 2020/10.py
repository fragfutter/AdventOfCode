#!/usr/bin/pypy3

from advent import Advent
from collections import defaultdict

"""
"""

def slicer(data):
    """split a list of adapters at 3V gaps into smaller lists"""
    data = sorted(data[:])  # make a copy we modify it
    s = [data.pop(0)]  # starting value
    while data:
        v = data.pop(0)
        if v - s[-1] == 3:
            yield s
            s = [v]  # start next
        else:
            s.append(v)
    yield s  # final


def path_count(data):
    """count possible paths from start to end.
    not using array indices, but knowing that the array is
    unique and sorted we can do all our tests with "in"
    """
    def search(start, end):
        nonlocal count
        if start == end:
            count += 1
            return
        if start not in data:
            return
        # the adaters that would fit are our_voltage + 1V,
        # our_voltage + 2V,  our_voltage + 3V
        # the test if we have this adapter available is done
        # in the recursive call, see right above.
        for i in range(1, 4):
            search(start + i, end)

    count = 0
    search(data[0], data[-1])
    return count


class Day(Advent):
    lines = True
    conversion = int

    def solve1(self):
        result = defaultdict(lambda: 0)
        device = max(self.data) + 3
        jolt = 0
        for a in sorted(self.data):
            assert(a - jolt <= 3)
            result[a - jolt] += 1
            jolt = a
        # our device
        result[3] += 1
        return result[1] * result[3]

    def solve2(self):
        """the idea is that at each 3V gap the problem can be divided in two
        as both adapters from the gap must be used.
        for the adapters of sample1:
        [0, 1], [4, 5, 6, 7], [10, 11, 12], [15, 16], [19], [22]
        the final solution is then the multiplication of each smaller problem.
        """
        data = self.data[:]
        data.append(0)  # starting voltage
        data.append(max(data) + 3)  # required end voltage
        result = 1
        for s in slicer(data):
            result = result * path_count(s)
        return result


Day.main()
