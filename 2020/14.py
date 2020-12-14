#!/usr/bin/pypy3

from advent import Advent
import re
from itertools import combinations

"""
"""

class BitMask(object):
    def __init__(self, mask):
        one = []
        zero = []
        floats = []
        v = 2**len(mask)
        for c in mask:
            v = v >> 1
            if c == 'X':
                floats.append(v)
            elif c == '1':
                one.append(v)
            else:
                zero.append(v)
        self.one = sum(one)
        self.zero = sum(zero)
        self.floats = floats

    def mask(self, value):
        result = value | self.one
        result = result - (result & self.zero)
        return result

    def float(self, value):
        result = value | self.one
        # now make a zero of all X/float
        result = result - (result & sum(self.floats))
        # now the floating bits in every permutation
        for i in range(len(self.floats) + 1):
            for combo in combinations(self.floats, i):
                yield result + sum(combo)


class Day(Advent):
    pat = re.compile(r'(?:mask|mem\[(\d+)\]) = (.*)$')

    def prepare(self):
        result = []
        for line in self.data.split('\n'):
            m = self.pat.match(line.strip())
            action, value = m.groups()
            if action:
                result.append((int(action), int(value)))
            else:
                result.append((None, BitMask(value)))
        self.data = result

    def solve1(self):
        registers = {}
        mask = None
        for reg, value in self.data:
            if reg is None:
                mask = value
                continue
            value = mask.mask(value)
            registers[reg] = value
        return sum(registers.values())

    def solve2(self):
        registers = {}
        mask = None
        for reg, value in self.data:
            if reg is None:
                mask = value
                continue
            for r in mask.float(reg):
                registers[r] = value
        return sum(registers.values())


Day.main()
