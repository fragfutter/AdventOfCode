#!/usr/bin/pypy3

from advent import Advent
from collections import defaultdict

"""
"""

class Day(Advent):
    def solve1(self):
        def start():
            return ''

        def end(result, group):
            group = set(group)  # unique
            result.append(group)
            return start()

        result = []
        group = start()
        for line in self.data.split('\n'):
            line = line.strip()
            if line == '':
                group = end(result, group)
                continue
            group += line
        end(result, group)

        return sum([len(x) for x in result])

    def solve2(self):
        def start():
            return defaultdict(lambda: 0)

        def end(result, group):
            result.append(group)
            return start()

        result = []
        group = start()
        for line in self.data.split('\n'):
            line = line.strip()
            if line == '':
                group = end(result, group)
                continue
            group['count'] +=1
            for c in line:
                assert(line.count(c) == 1)
                group[c] += 1
        end(result, group)

        value = 0
        for group in result:
            for key in filter(lambda x: x != 'count', group.keys()):
                if group[key] == group['count']:
                    value +=1
        return value


Day.main()
