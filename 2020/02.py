#!/usr/bin/pypy3

from advent import Advent
import re

"""
"""

class Day(Advent):
    lines = True
    pat = re.compile(r'(\d+)-(\d+) (.): (.*)')

    def conversion(self, line):
        min_, max_, char, password = self.pat.match(line).groups()
        return (int(min_), int(max_), char, password)

    def solve1(self):
        result = 0
        for min_, max_, char, password in self.data:
            c = password.count(char)
            if c >= min_ and c <= max_:
                result += 1
        return result

    def solve2(self):
        result = 0
        for min_, max_, char, password in self.data:
            a = password[min_ - 1]
            b = password[max_ - 1]
            if (a == char and b != char) or (a != char and b == char):
                result += 1
        return result


Day.main()
