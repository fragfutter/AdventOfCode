#!/usr/bin/pypy3

from advent import Advent
import re

"""
solution 1: 21993583522852
solution 2: 122438593522757
"""
class Calculator(object):
    pat_bracket = re.compile(r'\(([\d*+ ]+)\)')
    pat_op = re.compile(r'(\d+)\s*([+*])\s*(\d+)')
    pat_add = re.compile(r'(\d+)\s*\+\s*(\d+)')
    pat_mul = re.compile(r'(\d+)\s*\*\s*(\d+)')

    def __init__(self, part_two=False ):
        """
        find pattern we can solve and replace it with result
        repeat until nothing changes, then resolve next operator

        for part1, first search for anything that is in brackets
        and solve that sub-problem

        then resolve from left + and *

        for part2, brackets stay the same.
        then resolve all +
        and finally all *
        """
        if not part_two:
            self.tasks = (
                (self.pat_bracket, self.bracket),
                (self.pat_op, self.op),
            )
        else:
            self.tasks = (
                (self.pat_bracket, self.bracket),
                (self.pat_add, self.add),
                (self.pat_mul, self.multiply),
            )

    def bracket(self, m):
        return self.calc(m.group(1))

    def op(self, m):
        a, o, b = m.groups()
        a = int(a)
        b = int(b)
        if o == '+':
            result = a + b
        else:
            result = a * b
        return str(result)

    def multiply(self, m):
        result = int(m.group(1)) * int(m.group(2))
        return str(result)

    def add(self, m):
        result = int(m.group(1)) + int(m.group(2))
        return str(result)

    def calc(self, data):
        current = data
        for search, replace in self.tasks:
            while True:
                reduced = search.sub(replace, current, count=1)
                if reduced == current:
                    break
                current = reduced
        return current


class Day(Advent):
    lines = True

    def solve1(self):
        calculator = Calculator()
        result = 0
        for line in self.data:
            result += int(calculator.calc(line))
        return result

    def solve2(self):
        calculator = Calculator(part_two=True)
        result = 0
        for line in self.data:
            result += int(calculator.calc(line))
        return result


Day.main()
